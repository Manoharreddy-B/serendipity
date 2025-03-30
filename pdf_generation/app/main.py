# app/main.py

import logging
import sys

from .worker import consume_messages

def setup_logging():
    # Configure root logger or specific logger as needed
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout
    )

def run_worker():
    """
    Entry point for running the PDF generator worker.
    """
    setup_logging()
    consume_messages()

if __name__ == "__main__":
    run_worker()
