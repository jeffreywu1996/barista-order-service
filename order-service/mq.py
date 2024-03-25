import pika
import logging

from core.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)

class RabbitMQ:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.rabbitmq_server))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)



    def publish(self, message: str, routing_key: str = 'task_queue'):
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ))
        logger.info(f" [x] Sent {message}")
