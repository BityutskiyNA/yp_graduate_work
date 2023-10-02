"""Логгер."""

import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("django")
