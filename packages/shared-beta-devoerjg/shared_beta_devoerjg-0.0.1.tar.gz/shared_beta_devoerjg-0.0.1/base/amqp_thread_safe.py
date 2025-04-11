from threading import Thread, Lock
from datetime import datetime
import json
import time
import queue
import pika
import logging


class AmqpCommunication(Thread):
    """
     AMQP RabbitMQ 消息通道接口 (Thread-Safe)
    """

    def __init__(self, rabbitmq_ip, rabbitmq_port, rabbitmq_queue='example-queue', binding_key=None, ttl=21600000,
                 username='guest', password='guest', exchange='message-bus', exchange_type='topic',
                 heartbeat_interval=60):
        super(AmqpCommunication, self).__init__()
        
        self.rabbitmq_ip = rabbitmq_ip
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_queue = rabbitmq_queue
        self.username = username
        self.password = password
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.heartbeat_interval = heartbeat_interval
        self.binding_key = binding_key
        self.receive_message_queue = queue.Queue()
        self.connected = False
        self.ttl = ttl
        self.lock = Lock()  # Thread safety
        self.client = None
        self.connection = None

    def connect(self):
        """ Establish a connection to RabbitMQ (Thread-safe) """
        with self.lock:
            try:
                credentials = pika.PlainCredentials(self.username, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.rabbitmq_ip, port=self.rabbitmq_port, credentials=credentials,
                    heartbeat=self.heartbeat_interval
                )
                
                self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_connection_open,
                                                        on_close_callback=self.on_connection_closed)
                self.connection.ioloop.start()  # Start event loop
            except Exception as e:
                logging.error(f"Failed to connect to RabbitMQ: {e}")
                time.sleep(5)
                self.connect()  # Reconnect on failure

    def on_connection_open(self, connection):
        """ Callback when connection is opened """
        logging.info("Connection opened")
        self.connected = True
        self.client = self.connection.channel()
        self.setup_exchange()

    def on_connection_closed(self, connection, reason):
        """ Handles connection closure """
        logging.warning(f"Connection closed: {reason}")
        self.connected = False
        time.sleep(5)
        self.connect()

    def setup_exchange(self):
        """ Declares exchange and queue, then binds """
        with self.lock:
            self.client.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
            self.client.queue_declare(queue=self.rabbitmq_queue, durable=True, arguments={'x-message-ttl': self.ttl})
            for key in self.binding_key:
                self.client.queue_bind(exchange=self.exchange, queue=self.rabbitmq_queue, routing_key=key)

    def run(self):
        """ Starts consuming messages in a thread-safe manner """
        with self.lock:
            if not self.connected:
                self.connect()
            self.client.basic_consume(queue=self.rabbitmq_queue, on_message_callback=self.callback, auto_ack=True)
            try:
                self.client.start_consuming()
            except Exception as e:
                logging.error(f"{datetime.now()} pika lost connection, reconnecting: {e}")
                self.reconnect()

    def reconnect(self):
        """ Reconnect to RabbitMQ """
        with self.lock:
            self.close_connection()
            while not self.connected:
                try:
                    self.connect()
                    logging.info("Reconnected to RabbitMQ")
                    break
                except Exception as e:
                    logging.error(f"Reconnection failed: {e}, retrying in 5 seconds...")
                    time.sleep(5)

    def close_connection(self):
        """ Close the RabbitMQ connection """
        with self.lock:
            if self.connection and self.connection.is_open:
                self.connection.close()

    def callback(self, ch, method, properties, body):
        """ Message callback function """
        try:
            message = json.loads(body)
            self.receive_message_queue.put(message)
        except Exception as e:
            logging.error(f"Message Callback Error {e}")

    def send_message(self, message, routing_key, exchange=None, is_already_json=False):
        """ Send a message to RabbitMQ (Thread-safe) """
        with self.lock:
            if not exchange:
                exchange = self.exchange
            try:
                if not is_already_json:
                    message = json.dumps(message)
                self.client.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
                logging.info(f"Sent message to {exchange} routing_key: {routing_key}")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
