import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pika.exceptions import ChannelWrongStateError

from src.db.publish_to_storage import RabbitPublisher, RabbitPublisherAsync
from src.models.notification import (
    NotificationByEventType,
    NotificationBySpecificEvent,
    NotificationByTypeOfMessage,
    NotificationRegisteredUser,
)

from src.service.shortener_service import shortener_service

router = APIRouter()

db = RabbitPublisherAsync()


@router.post(
    "/send_to_queue_by_type_of_message", name="Отправка в очередь по типу сообщения"
)
async def send_to_queue_by_type_of_message(payload: NotificationByTypeOfMessage):
    try:
        await db.create_queues()
    except ChannelWrongStateError:
        return JSONResponse({"message": "failed"}, status_code=400)

    await db.send_to_queue_by_type_of_message(
        message=payload, queue="queue_by_type_of_message"
    )
    return JSONResponse({"message": "ok"}, status_code=200)


@router.post(
    "/send_to_queue_by_specific_event",
    name="Отправка в очередь по определенному событию",
)
async def send_to_queue_by_specific_event(payload: NotificationBySpecificEvent):
    try:
        await db.create_queues()
    except ChannelWrongStateError:
        return JSONResponse({"message": "failed"}, status_code=400)

    await db.send_to_queue_by_specific_event(
        message=payload, queue="queue_by_specific_event"
    )

    return JSONResponse({"message": "ok"}, status_code=200)


async def send_to_queue_for_a_specific_event_urgent(
    payload: NotificationBySpecificEvent,
):
    try:
        await db.create_queues()
    except ChannelWrongStateError:
        return JSONResponse({"message": "failed"}, status_code=400)

    await db.send_to_queue_for_a_specific_event_urgent(
        message=payload, queue="queue_for_a_specific_event_urgent"
    )

    return JSONResponse({"message": "ok"}, status_code=200)


@router.post("/send_to_queue_by_event_type", name="Отправка в очередь по типу события")
async def send_to_queue_by_event_type(payload: NotificationByEventType):
    try:
        await db.create_queues()
    except ChannelWrongStateError:
        return JSONResponse({"message": "failed"}, status_code=400)

    await db.send_to_queue_by_event_type(message=payload, queue="queue_by_event_type")
    return JSONResponse({"message": "ok"}, status_code=200)


@router.post(
    "/send_to_queue_by_event_type_urgent",
    name="Отправка в очередь по типу события - срочная",
)
async def send_to_queue_by_event_type_urgent(payload: NotificationByEventType):
    try:
        await db.create_queues()
    except ChannelWrongStateError:
        return JSONResponse({"message": "failed"}, status_code=400)

    await db.send_to_queue_by_event_type_urgent(
        message=payload, queue="queue_by_event_type_urgent"
    )
    return JSONResponse({"message": "ok"}, status_code=200)


@router.post(
    "/send_to_queue_registration_event",
    name="Отправка в очередь при регистрации пользователя",
)
async def send_to_queue_registration_event(payload: NotificationRegisteredUser):
    if payload.registration_link:
        response = shortener_service().get_short_url(
            long_link=payload.registration_link
        )
        response_data = response.json()
        if response_data["success"]:
            payload.registration_link = response_data["short_url"]

            try:
                await db.create_queues()
            except ChannelWrongStateError:
                return JSONResponse({"message": "failed"}, status_code=400)

            await db.send_to_queue_registration_event(
                message=payload, queue="queue_registration_event"
            )
            return JSONResponse({"message": "ok"}, status_code=200)

        return JSONResponse({"message": "failed"}, status_code=400)
