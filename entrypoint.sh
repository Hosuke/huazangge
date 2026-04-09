#!/bin/bash
# /app/data is the Railway volume mount point

if [ ! -f /app/data/.initialized ]; then
    echo "First boot: initializing persistent data volume..."
    mkdir -p /app/data/raw /app/data/wiki/concepts /app/data/wiki/_meta /app/data/wiki/outputs
    if [ -d /app/seed/wiki ]; then
        cp -r /app/seed/wiki/* /app/data/wiki/ 2>/dev/null || true
    fi
    touch /app/data/.initialized
    echo "Volume initialized."
else
    echo "Volume already initialized. Merging progress files..."
    # ALWAYS merge progress/compiled_sources from seed (newer = more complete)
    for f in compiled_sources.json cbeta_progress.json wikisource_progress.json; do
        seed="/app/seed/wiki/_meta/$f"
        vol="/app/data/wiki/_meta/$f"
        if [ -f "$seed" ]; then
            if [ -f "$vol" ]; then
                # Merge: keep the one with more entries
                seed_size=$(wc -c < "$seed")
                vol_size=$(wc -c < "$vol")
                if [ "$seed_size" -gt "$vol_size" ]; then
                    cp "$seed" "$vol"
                    echo "  Updated $f from seed (larger)"
                fi
            else
                cp "$seed" "$vol"
                echo "  Copied $f from seed"
            fi
        fi
    done
    # Also update wiki articles: only add new ones from seed, never overwrite
    if [ -d /app/seed/wiki/concepts ]; then
        cp -rn /app/seed/wiki/concepts/* /app/data/wiki/concepts/ 2>/dev/null || true
    fi
fi

ln -sfn /app/data/raw /app/raw
ln -sfn /app/data/wiki /app/wiki

# /dev/shm is a tmpfs that avoids slow disk I/O for gunicorn worker heartbeat
# files; fall back to /tmp if it isn't available or writable in this runtime.
WORKER_TMP_DIR_ARG=""
if [ -d /dev/shm ] && [ -w /dev/shm ]; then
    WORKER_TMP_DIR_ARG="--worker-tmp-dir /dev/shm"
fi

exec gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers 2 --threads 2 \
    --timeout 120 --graceful-timeout 30 \
    ${WORKER_TMP_DIR_ARG} \
    --access-logfile - \
    wsgi:app
