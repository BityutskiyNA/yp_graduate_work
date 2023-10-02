import asyncio

from worker.src.services.process_queue import process_queue_by_type_of_message, process_queue_by_specific_event, \
    process_queue_by_event_type, process_queue_for_postponed_messages, \
    process_queue_by_event_type_urgent, process_queue_by_specific_event_urgent
from worker.src.services.queue_consumer import QueueConsumer

if __name__ == "__main__":
    consumer1 = QueueConsumer('queue_by_type_of_message', process_queue_by_type_of_message)
    consumer2 = QueueConsumer('queue_by_specific_event', process_queue_by_specific_event)
    consumer3 = QueueConsumer('queue_by_event_type', process_queue_by_event_type)

    consumer4 = QueueConsumer('queue_for_a_specific_event_urgent', process_queue_by_specific_event_urgent)
    consumer5 = QueueConsumer('queue_by_type_of_message_urgent', process_queue_by_event_type_urgent)
    consumer6 = QueueConsumer('queue_by_event_type_urgent', process_queue_by_event_type_urgent)

    consumer7 = QueueConsumer('queue_registration_event', process_queue_by_event_type)

    consumer8 = QueueConsumer('queue_for_postponed_messages', process_queue_for_postponed_messages)
    consumer9 = QueueConsumer('queue_for_error_messages', process_queue_for_postponed_messages)
    try:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(consumer1.run()),
            loop.create_task(consumer2.run()),
            loop.create_task(consumer3.run()),
        ]
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()
