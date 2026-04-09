"""WSGI entry point for 华藏阁.

Wires the deployment-specific concerns that llmbase intentionally leaves
to downstream projects:

1. **Hooks**: register callbacks on llmbase lifecycle events so that every
   ingest / compile is mirrored to the remote sync table (Supabase).
2. **Cross-process worker dedup**: when gunicorn runs ``--workers > 1``,
   each worker process imports this file and would otherwise spawn its own
   daemon thread. We hold an advisory ``fcntl`` lock on
   ``/tmp/huazangge_worker.lock`` so only one process runs the daemon.
3. **Worker daemon startup** — same as before, fail-soft.

llmbase core stays pure: no Supabase code, no fcntl, no Railway specifics.
"""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("huazangge.wsgi")

base = Path(__file__).resolve().parent

# ─── Register llmbase hooks → remote sync ──────────────────────────────────
# llmbase core emits "ingested" / "compiled" events; we forward them
# directly to a PostgREST-compatible sync table (Supabase). The upsert is
# inlined here rather than calling tools.sync.push_ingested/mark_compiled,
# because llmbase 0.2.x's helpers are missing the on_conflict query
# parameter — see _sync_upsert() below for the workaround. Hooks are
# best-effort — exceptions inside callbacks are caught by llmbase and
# logged at warning, never disrupting the core ingest/compile loop.
try:
    from tools.hooks import register
    from datetime import datetime, timezone
    import requests

    # NOTE: llmbase 0.2.x ships tools/sync.py but its push_ingested /
    # mark_compiled don't pass `?on_conflict=source,work_id` on the
    # PostgREST POST, so any second write for an existing (source,work_id)
    # row gets rejected with HTTP 409 "duplicate key violates unique
    # constraint". That makes mark_compiled a permanent no-op against the
    # current Supabase schema. Until llmbase upstream is patched, we do
    # the upsert inline here with the correct on_conflict parameter.

    _SYNC_URL = (os.environ.get("LLMBASE_SYNC_URL", "")
                 or os.environ.get("SUPABASE_URL", "")).rstrip("/")
    _SYNC_KEY = (os.environ.get("LLMBASE_SYNC_KEY", "")
                 or os.environ.get("SUPABASE_KEY", ""))
    _SYNC_TABLE = os.environ.get("LLMBASE_SYNC_TABLE", "huazangge_ingested")
    _SYNC_TIMEOUT = 8

    def _sync_upsert(payload: dict) -> None:
        """Upsert one row into the remote sync table.

        Best-effort: any failure (network, auth, schema mismatch) is logged
        at warning and swallowed so a flapping Supabase cannot stall the
        worker. The on_conflict query parameter is required for PostgREST
        to honour the unique constraint as a merge key on POST.
        """
        if not (_SYNC_URL and _SYNC_KEY):
            return
        try:
            resp = requests.post(
                f"{_SYNC_URL}/rest/v1/{_SYNC_TABLE}"
                "?on_conflict=source,work_id",
                json=payload,
                headers={
                    "apikey": _SYNC_KEY,
                    "Authorization": f"Bearer {_SYNC_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "resolution=merge-duplicates,return=minimal",
                },
                timeout=_SYNC_TIMEOUT,
            )
            if resp.status_code not in (200, 201, 204):
                logger.warning(
                    f"[hooks] sync upsert {payload.get('source')}/"
                    f"{payload.get('work_id')} → HTTP {resp.status_code}: "
                    f"{resp.text[:200]}"
                )
        except Exception as e:
            logger.warning(
                f"[hooks] sync upsert {payload.get('source')}/"
                f"{payload.get('work_id')} failed: {e}"
            )

    def _on_ingested(source, work_id, title=None, **_):
        _sync_upsert({
            "source": source,
            "work_id": work_id,
            "title": title or None,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        })

    def _on_compiled(source, work_id, **_):
        if not work_id:
            return
        _sync_upsert({
            "source": source,
            "work_id": work_id,
            "compiled": True,
            "compiled_at": datetime.now(timezone.utc).isoformat(),
        })

    register("ingested", _on_ingested)
    register("compiled", _on_compiled)

    if _SYNC_URL and _SYNC_KEY:
        logger.info(f"[hooks] Remote sync enabled → {_SYNC_TABLE} "
                    "(ingested + compiled events mirrored to Supabase)")
    else:
        logger.warning("[hooks] Sync env vars not set "
                       "(LLMBASE_SYNC_URL / LLMBASE_SYNC_KEY) — "
                       "hooks registered but no-op")
except ImportError as e:
    logger.warning(f"[hooks] Could not wire sync hooks: {e}")

# ─── Cross-process worker daemon dedup (gunicorn --workers > 1) ────────────
# llmbase 0.2.x removed fcntl from core and asked downstream to add its own
# locking. Without this guard, gunicorn would spawn one worker daemon per
# process and we'd get concurrent learn/compile races on the same files.
_pidlock_handle = None  # Module scope keeps the lock fd alive for process lifetime


def _try_acquire_worker_lock() -> bool:
    """Acquire a non-blocking advisory lock on the worker daemon slot.

    Returns True iff this process should run the daemon. The kernel
    auto-releases the lock when the process exits, so a crashed gunicorn
    worker correctly hands the slot to the next one that gets forked.

    Failure modes are **fail-closed**: if anything in the locking machinery
    breaks (cannot open lockfile, ``flock`` syscall errors, etc.) we refuse
    to start the daemon rather than risk multiple gunicorn workers each
    spawning their own daemon and racing on shared files. The operator
    will see a warning in container logs and can investigate / restart.
    The only safe degradation path is non-POSIX (Windows dev), where there
    is only ever one process and the in-process guard is sufficient.
    """
    global _pidlock_handle
    try:
        import fcntl
    except ImportError:
        # Non-POSIX (Windows dev) — single process, in-process guard suffices
        return True

    lock_path = "/tmp/huazangge_worker.lock"
    try:
        handle = open(lock_path, "w")
    except OSError as e:
        logger.error(
            f"[worker-lock] Could not open {lock_path}: {e}. "
            "REFUSING to start daemon to avoid cross-process race. "
            "Investigate /tmp permissions and restart."
        )
        return False

    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        logger.info("[worker-lock] Daemon already running in another process")
        return False
    except OSError as e:
        handle.close()
        logger.error(
            f"[worker-lock] flock() failed: {e}. "
            "REFUSING to start daemon to avoid cross-process race."
        )
        return False

    # Hand the open file to module scope so the kernel keeps the lock
    _pidlock_handle = handle
    try:
        handle.write(str(os.getpid()))
        handle.flush()
    except OSError:
        pass  # PID write is debug only
    return True


# ─── Build app + start worker ──────────────────────────────────────────────
from tools.web import create_web_app
app = create_web_app(base)

if _try_acquire_worker_lock():
    try:
        from tools.worker import start_worker_thread
        start_worker_thread(base)
        logger.info("[worker] Daemon thread started")
    except ImportError:
        logger.warning("[worker] Module not available, running in serve-only mode")
