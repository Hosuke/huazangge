"""WSGI entry point for 华藏阁."""
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

base = Path(__file__).resolve().parent

# Import from installed llmbase package
from tools.web import create_web_app
app = create_web_app(base)

# Try to start worker (graceful if not available)
try:
    from tools.worker import start_worker_thread
    start_worker_thread(base)
except ImportError:
    logging.warning("Worker module not available, running in serve-only mode")
