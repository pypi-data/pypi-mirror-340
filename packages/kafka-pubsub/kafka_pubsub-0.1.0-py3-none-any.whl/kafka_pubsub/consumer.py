import logging

from confluent_kafka import Consumer as KafkaConsumerClient, KafkaError

from kafka_pubsub.utils import kafka_topics_prefix
from kafka_pubsub.conf import Conf

class Consumer:
    def __init__(self, topic='default', config=None):
        self.topic = kafka_topics_prefix() + topic
        self.config = Conf.set_consumer_config(config)
        self.consumer = KafkaConsumerClient(self.config)
        self.consumer.subscribe([self.topic])
        logging.info(f"🔄 Subscribed to topic: {self.topic}")

    def get_topic(self):
        return self.topic

    def poll(self, timeout=1.0):
        msg = self.consumer.poll(timeout)
        if msg is None:
            return None
        if msg.error():
            code = msg.error().code()
            if code == KafkaError._PARTITION_EOF:
                logging.debug("📦 End of partition reached")
                return None
            elif code == KafkaError._TIMED_OUT:
                logging.debug("⏳ Poll timed out")
                return None
            else:
                raise Exception(f"[Kafka Error] {msg.error()}")
        return msg

    def process(self, message):
        print(f"[Message] {message.value().decode('utf-8')}")

    def commit(self, msg):
        self.consumer.commit(msg)
        logging.info("✅ Committed offset")

    def close(self):
        self.consumer.close()

    def on_message_success(self, msg):
        pass

    def on_message_failure(self, msg, error):
        pass

    
