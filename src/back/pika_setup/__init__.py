import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

class PikaConnection:
    pika_connection:BlockingConnection = None
    channel: BlockingChannel = None

    @classmethod
    def startup(cls):
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        PikaConnection.pika_connection = connection
        PikaConnection.channel = channel
