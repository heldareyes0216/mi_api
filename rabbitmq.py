import pika
import json

RABBITMQ_HOST = "rabbitmq"


def enviar_mensaje(mensaje):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.queue_declare(
        queue="products",
        durable=True
    )

    channel.basic_publish(
        exchange="",
        routing_key="products",
        body=json.dumps(mensaje),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()

    print("Mensaje enviado a RabbitMQ")