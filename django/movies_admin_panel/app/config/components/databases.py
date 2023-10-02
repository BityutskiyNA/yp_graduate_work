from src.core.config import config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.db.database,
        "USER": config.db.user,
        "PASSWORD": config.db.password,
        "HOST": config.docker.db_host,
        "PORT": config.db.port,
        "OPTIONS": {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            "options": "-c search_path=public,content"
        },
    }
}
