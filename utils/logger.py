import logging
import sys
from pathlib import Path

LOG_DIR  = Path(__file__).parent.parent / "output"
LOG_FILE = LOG_DIR / "pipeline.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=_FMT,
    datefmt=_DATE_FMT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
