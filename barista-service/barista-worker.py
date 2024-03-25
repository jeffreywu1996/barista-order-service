import pika
import json
import time
import logging
import requests

# from config import settings
from menu import mapping

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
logger.info('Barista Worker started')
logger.info(' [*] Waiting for messages. To exit press CTRL+C')


def update_order_status(order_id, status):
    url = f"http://order-service:8000/v1/order/{order_id}"
    data = {"status": status}
    response = requests.put(url, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to update order: {response.text}")

    return response.json()

def callback(ch, method, properties, body):
    logger.info(f" [x] Received {body.decode()}")
    bodyd = json.loads(body.decode())
    coffee_type = bodyd.get('coffee_type')
    uuid = bodyd.get('id')
    if coffee_type not in mapping:
        logger.error(f" [x] Invalid coffee type: {coffee_type}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    time_to_prepare = mapping.get(coffee_type)['time_to_make']
    logger.info(f" [x] Making {coffee_type} for {time_to_prepare} seconds")
    time.sleep(time_to_prepare)

    logger.info(f" [x] Done ({uuid})")

    # Make request to order-service to update order status
    update_order_status(uuid, 'completed')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
