"""Модуль с настройками django проекта."""

# импорт библиотек
from pathlib import Path

from split_settings.tools import include
from src.core.config import config

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# секрет джанго
SECRET_KEY = config.django.secret_key
# режим запуска
DEBUG = config.django.debug

# доступные порты в режиме деплоя (DEBUG=False)
ALLOWED_HOSTS = config.django.allowed_hosts.split(",")
# для панели дебага
INTERNAL_IPS = config.django.internal_ips.split(",")

# контроллеры
ROOT_URLCONF = "config.urls"
# вебсервер
WSGI_APPLICATION = "config.wsgi.application"

# компоненты, выведенные в отдельный модуль
include(
    "components/databases.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/auth_password_validators.py",
)

# язык
LANGUAGE_CODE = "ru-RU"

# время
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# директория со статическими файлами
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# директория с локализацией
LOCALE_PATHS = ["src/locale"]
