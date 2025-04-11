
from kafka_pubsub.config.pubsub import KAFKA_CONFIG
from kafka_pubsub.producer import Producer

def kafka_produce(topic, data, key=None):
    producer = Producer()
    producer.produce(topic, data, key)
    producer.flush()

def kafka_topics_prefix():
    return KAFKA_CONFIG.get('topics_prefix')
