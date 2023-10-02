import requests

from src.core.config import app_settings


class ShortenerService:
    @staticmethod
    def get_short_url(long_link: str):
        session = requests.Session()
        session.trust_env = False
        response = session.post(app_settings.shortener_link, json={"url": long_link})
        return response


def shortener_service() -> ShortenerService:
    return ShortenerService()
