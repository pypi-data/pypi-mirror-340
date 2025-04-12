# kafka_lib/producer.py
import json

from confluent_kafka import Producer as KafkaProducerClient
from kafka_pubsub.conf import Conf

class Producer:

    def __init__(self, config=None):
        config = config or Conf.set_producer_config()
        self.producer = KafkaProducerClient(config)

    def produce(self, topic, data: dict, key=None):
        try:
            value = json.dumps(data).encode("utf-8")  # 🔄 Always serialize dict to bytes
            key_bytes = key.encode("utf-8") if key else None

            self.producer.produce(
                topic=topic,
                value=value,
                key=key_bytes,
                callback=self.delivery_report
            )
            self.producer.poll(0)
        except Exception as e:
            print(f"[ERROR] Failed to produce to topic {topic}: {e}")

    def flush(self):
        while self.producer.flush(0) > 0:
            self.producer.poll(0.05)

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print(f"[ERROR] Delivery failed: {err}")
        else:
            print(f"[INFO] Delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")
