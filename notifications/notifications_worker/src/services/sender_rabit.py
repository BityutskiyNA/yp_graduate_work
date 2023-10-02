import pika

from worker.config import app_settings_rabbit


rabbitmq_host = app_settings_rabbit.rabbitmq_host
rabbitmq_port = app_settings_rabbit.rabbitmq_port
rabbitmq_virtual_host = app_settings_rabbit.rabbitmq_virtual_host
rabbitmq_username = app_settings_rabbit.rabbitmq_username
rabbitmq_password = app_settings_rabbit.rabbitmq_password

credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
connection_params = pika.ConnectionParameters(host=rabbitmq_host,
                                              port=rabbitmq_port,
                                              virtual_host=rabbitmq_virtual_host,
                                              credentials=credentials)

connection = pika.BlockingConnection(connection_params)


def send_to_qulle(message_data, queue_name):
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_data)
    finally:
        connection.close()
