#!/usr/bin/env python
import pika
import json
import importlib
import signal
import sys

from constants import RABBITMQ_HOST


QUEUE_NAME = 'translate-hindi'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()


def sigterm_handler(*args):
    print("Received TERM signal. Closing the channel and connection")
    channel.close()
    connection.close()
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)


channel.queue_declare(queue=QUEUE_NAME, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body = body.decode()
    # Expecting the body to be json with the following keys:
    # full function name, args
    print(f"Received {body}")
    try:
        body = json.loads(body)
        assert 'module_name' in body
        assert 'function_name' in body
        assert 'args' in body
    except Exception as e:
        # TODO: Log as an exception
        print(f"Some keys missing. {e}")
        # But still acknowledge to evict this entry from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return None
    module_name = body['module_name']
    function_name = body['function_name']
    args = body['args']
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        # TODO: Log as an exception
        print(f"Exception {e} in importing module {module_name}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return None
    try:
        func = getattr(module, function_name)
    except Exception as e:
        print(f"Exception {e} in getting function {function_name} from {module_name}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return None
    try:
        # func(*args)
        print("Skipping function for now")
    except Exception as e:
        print(f"Exception {e} while running the function")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        pass
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=3)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

channel.start_consuming()
