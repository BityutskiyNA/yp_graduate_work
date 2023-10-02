import logging.config

from .config import Settings, get_settings
from .logger import LOGGING_SETTINGS

base_config: Settings = get_settings()

# Применяем настройки логирования
logging.config.dictConfig(LOGGING_SETTINGS)
logging.getLogger().setLevel(base_config.logging_level)
