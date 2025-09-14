from __future__ import annotations
import logging
from typing import Optional
_LOGGER_NAME = "aioworxmower"

def get_logger(name: Optional[str] = None) -> logging.Logger:
    full = _LOGGER_NAME + (f".{name}" if name else "")
    logger = logging.getLogger(full)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    return logger

def set_level(level: int | str) -> None:
    lvl = logging.getLevelName(level) if isinstance(level, str) else level
    logging.getLogger(_LOGGER_NAME).setLevel(lvl)
    for name, logger in logging.Logger.manager.loggerDict.items():  # type: ignore[attr-defined]
        if isinstance(logger, logging.Logger) and name.startswith(_LOGGER_NAME):
            logger.setLevel(lvl)
