from threading import Thread
from datetime import datetime
import json
import time
import queue
import pika
import logging


class AmqpCommunication(Thread):
    """
     AMQP RabbitMQ 消息通道接口

    """

    def __init__(self, rabbitmq_ip, rabbitmq_port, rabbitmq_queue='example-queue', binding_key=None, ttl=21600000,
                 username='guest', password='guest', exchange='message-bus', exchange_type='topic',
                 heartbeat_interval=60):
        super(AmqpCommunication, self).__init__()
        """
        :param rabbitmq_ip:            登入RabbitMQ服務器的ip
        :param rabbitmq_port:          登入RabbitMQ服務器的port
        :param rabbitmq_queue:         RabbitMQ服務器指定的分配消息對列
        :params ttl:                   RabbitMQ消息TTL
        :param username:               登入RabbitMQ服務器的用戶名
        :param password:               登入RabbitMQ服務器的密碼
        :param exchange:               指定的交換機名稱
        :param exchange_type:          指定的交換機類型
        :param heartbeat_interval:     心跳間隔:指超過此時間間隔不心跳或消息 server主動斷開連接  
        "param binding_key:            RabbitMQ queue所指定路由鍵
        """
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
        self.client, self.connection = self.__connector()

    def __connector(self):
        """
        create the AMQP RabbitMQ connection instance 
        """
        try:
            channel, connection = None, None
            while not channel or not connection:
                try:
                    credentials = pika.PlainCredentials(self.username, self.password)
                    args = {'x-message-ttl': self.ttl}
                    print("Try to connect to RABBITBQ: ", self.rabbitmq_ip, self.rabbitmq_port, self.username, self.password)
                    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=self.rabbitmq_ip, port=self.rabbitmq_port, credentials=credentials,
                                                heartbeat=self.heartbeat_interval))

                    channel = connection.channel()
                    channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
                    channel.queue_declare(queue=self.rabbitmq_queue, durable=True, arguments=args)
                    for cur_queue in self.binding_key:
                        channel.queue_bind(exchange=self.exchange, queue=self.rabbitmq_queue, routing_key=cur_queue)

                    # Add connection blocked and unblocked callbacks
                    connection.add_on_connection_blocked_callback(self.on_connection_blocked)
                    connection.add_on_connection_unblocked_callback(self.on_connection_unblocked)

                except Exception as e:
                    print(f"Failed to connect to RabbitMQ: {e}")
                    logging.error(f"Failed to connect to RabbitMQ: {e}")
                    time.sleep(5)

            logging.info(f"connect to rabbitmq")
            print(f"connect to rabbitmq")
            return channel, connection

        except Exception as e:
            print(f"connect to the RabbitMQ occur error {e}")

    def close_connection(self):
        """
        :param connection: a rabbitmq client connection instance
        """
        if self.connection and self.connection.is_open:
            self.connection.close()

    def delete_queue(self, queue):
        """
        :param queue:  the name of queue would be deleted
        """
        self.client.queue_delete(queue=queue)

    def delete_exchange(self, exchange):
        """
        :param exchange:  the name of exchange would be deleted
        """
        self.client.exchange_delete(exchange=exchange)

    def callback(self, ch, method, properties, body):
        """
        receive RabbitMQ messages callback function
        :param body:  receive messages
        """
        try:
            message = json.loads(body)
            self.receive_message_queue.put(message)
        except Exception as e:
            print(f"Message Callback Error {e}")

    def check_exchange_exists(self, exchange_name):
        # Establish temp connection
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host = self.rabbitmq_ip, port = self.rabbitmq_port, credentials = credentials, 
                                      heartbeat = self.heartbeat_interval))
        channel = connection.channel()

        # Try to declare an exchange to check its existence
        try: 
            channel.exchange_declare(exchange=exchange_name, exchange_type="topic", passive=True) 
            print(f"Check Exchange with type <topic> -- Exchange: <'{exchange_name}'> exists.") 
            return True
        except Exception as e: 
            print(f"Check Exchange with type <topic> -- Exchange: <'{exchange_name}'> does not exist.\nMsg:{e}") 
            return False
        finally:
            connection.close()

    def run(self):
        self.client.basic_consume(queue=self.rabbitmq_queue, on_message_callback=self.callback, auto_ack=True)
        while True:
            try:
                self.client.start_consuming()
            except Exception as e:
                print(f"{datetime.now()} pika lost connection, reconnecting to the broker: {e}")
                self.reconnect()

    def on_connection_blocked(self, connection, reason):
        logging.warning(f"Connection blocked: {reason}")

    def on_connection_unblocked(self, connection):
        logging.info("Connection unblocked")

    def reconnect(self):
        self.close_connection()
        while True:
            try:
                self.client, self.connection = self.__connector()
                self.client.basic_consume(queue=self.rabbitmq_queue, on_message_callback=self.callback, auto_ack=True)
                logging.info("Reconnected to RabbitMQ")
                break
            except Exception as e:
                logging.error(f"Reconnection failed: {e}, retrying in 5 seconds...")
                time.sleep(5)

    def send_message(self, message, routing_key, exchange=None, is_already_json=False):
        """
        Send a message to RabbitMQ.
        :param message: The message to be sent.
        :param routing_key: The routing key for the message.
        """
        if not exchange:
            exchange = self.exchange
        try:
            if not is_already_json:
                message = json.dumps(message)

            self.client.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
            print(f"Sent message to {exchange} routing_key: {routing_key}")
            logging.info(f"Sent message to {exchange} routing_key: {routing_key}")
        except Exception as e:
            print(f"Failed to send message to {self.rabbitmq_queue}, error: {e}, message: {message}")
            logging.error(f"Failed to send message: {e}")

    def stop(self):
        self.client.stop_consuming()
        self.client.close()
        print("Stop AMQP Communication")
        logging.info("Stop AMQP Communication")


if __name__ == '__main__':
    # client1 = AmqpCommunication('10.146.212.85', 30024, 'edge-pqm-indicators')
    # client1.start()

    # receive = AmqpCommunication('10.146.212.85', 30025, 'edge-pqm-indicators', 'guest', 'guest')
    # receive.start()

    routing_key = ['eda.data.edgexevent.#']
    sender = AmqpCommunication('10.146.212.85', 30025, 'srv-elasticsearch-adapter', routing_key, 21600000)

    # Send a large message to demo 
    large_message = {"data": "X" * 10}  # Example large message
    sender.run()
