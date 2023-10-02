import asyncio

from worker.src.services.message import Message
import json
import requests

from worker.src.services.model import DataMail

from notifications.notifications_worker.config import app_settings

semaphore = asyncio.Semaphore(18)


async def process_queue_by_url(url, data, urgent=False):
    async with semaphore:
        django_response = requests.get(url)
        django_response_json = json.loads(django_response)

        user_url = data.get('user_url', None)
        if user_url:
            user_response = requests.get(user_url)
            user_response_json = json.loads(user_response)
        else:
            user_response_json = {}
        if django_response_json['agent'] == 'mail':
            mailing_data = DataMail(**django_response_json, **user_response_json)
            send_message = Message(mailing_data)
            send_message.send_message()
    if not urgent:
        await asyncio.sleep(5)


async def process_queue_by_type_of_message(message):
    js_ms = json.loads(message.decode('utf-8'))
    type_id = js_ms['mailing_type']
    django_url = f"{app_settings.mailing_mailing_type}{type_id}"
    user_url =  f"{app_settings.notification_getbytype}{type_id}"

    await process_queue_by_url(django_url, {'user_url': user_url})


async def process_queue_by_specific_event(message):
    js_ms = json.loads(message.decode('utf-8'))
    id_event = js_ms['event_type']
    django_url = f"{app_settings.mailing_system_events}{id_event}"
    user_id = js_ms['user_id']
    user_url = f"{app_settings.notification_getbyid}{user_id}"

    await process_queue_by_url(django_url, {'user_url': user_url})


async def process_queue_by_event_type(message):
    js_ms = json.loads(message.decode('utf-8'))
    id_event = js_ms['event_type']
    django_url = f"{app_settings.mailing_system_events}{id_event}"
    user_url = f"{app_settings.notification_getbytype}{id_event}"

    await process_queue_by_url(django_url, {'user_url': user_url})


async def process_queue_for_postponed_messages(message):
    js_ms = json.loads(message.decode('utf-8'))
    mail_data = DataMail(**js_ms)
    send_message = Message(mail_data)
    send_message.send_message()


async def process_queue_registration_event(message):
    js_ms = json.loads(message.decode('utf-8'))
    id_event = js_ms['event_type']
    django_url = f"{app_settings.mailing_system_events}{id_event}"
    user_id = js_ms['user_id']
    user_url = f"{app_settings.notification_getbyid}{user_id}"

    await process_queue_by_url(django_url, {'user_url': user_url})


async def process_queue_by_type_of_message_urgent(message):
    js_ms = json.loads(message.decode('utf-8'))
    type_id = js_ms['mailing_type']
    django_url =f"{app_settings.mailing_mailing_type}{type_id}"
    user_url = f"{app_settings.notification_getbytype}{type_id}"

    await process_queue_by_url(django_url, {'user_url': user_url}, urgent=True)


async def process_queue_by_specific_event_urgent(message, urgent=True):
    js_ms = json.loads(message.decode('utf-8'))
    id_event = js_ms['event_type']
    django_url = f"{app_settings.mailing_system_events}{id_event}"
    user_id = js_ms['user_id']
    user_url = f"{app_settings.notification_getbyid}{user_id}"

    await process_queue_by_url(django_url, {'user_url': user_url})


async def process_queue_by_event_type_urgent(message, urgent=True):
    js_ms = json.loads(message.decode('utf-8'))
    id_event = js_ms['event_type']
    django_url = f"{app_settings.mailing_system_events}{id_event}"
    user_url = f"{app_settings.notification_getbytype}{id_event}"

    await process_queue_by_url(django_url, {'user_url': user_url})
