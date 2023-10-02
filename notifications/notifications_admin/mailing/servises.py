import requests

from notifications.notifications_admin.config import AppSettings


def send_data_to_fastapi(data):
    fastapi_url = AppSettings.fastapi_url
    response = requests.post(fastapi_url, json=data)

    return response.status_code
