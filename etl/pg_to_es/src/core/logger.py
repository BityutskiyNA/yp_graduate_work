"""Логгер."""

import logging
from pathlib import Path


def get_logger(iteration: int) -> logging.Logger:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    logging.basicConfig(
        encoding="utf-8",
        format="%(asctime)s %(message)s",
        level=logging.INFO,
    )
    return logging.getLogger("etl")
