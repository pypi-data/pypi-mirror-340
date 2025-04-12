# config/kafka.py

import os
from kafka_pubsub.config.utils import get_bool_env

KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'security_protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
    'sasl_mechanisms': os.getenv('KAFKA_SASL_MECHANISMS', 'PLAIN'),
    'sasl_username': os.getenv('KAFKA_SASL_USERNAME', ''),
    'sasl_password': os.getenv('KAFKA_SASL_PASSWORD', ''),
    'consumer_group': os.getenv('KAFKA_CONSUMER_GROUP', 'default-group'),
    'topics_prefix': os.getenv('KAFKA_TOPICS_PREFIX', ''),
    'auto_offset_reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', 'earliest'),
    'enable_auto_commit': get_bool_env('KAFKA_ENABLE_AUTO_COMMIT', False),
    'message_send_max_retries': int(os.getenv('KAFKA_MESSAGE_SEND_MAX_RETRIES', 5)),
    'max_poll_interval_ms': int(os.getenv('KAFKA_MAX_POLL_INTERVAL_MS', 90000)),
    'debug': os.getenv('KAFKA_DEBUG', None),
    'poll_sleep_ms': int(os.getenv('KAFKA_POLL_SLEEP_MS', 100)),

}
