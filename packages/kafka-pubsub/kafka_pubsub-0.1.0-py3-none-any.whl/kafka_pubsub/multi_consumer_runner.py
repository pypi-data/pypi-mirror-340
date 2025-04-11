import logging
import time
from kafka_pubsub.config.pubsub import KAFKA_CONFIG
from kafka_pubsub.conf import Conf

class MultiConsumerRunner:

    @staticmethod
    def run(consumer_classes, consumer_configs=None):
        consumer_configs = consumer_configs or {}
        consumers = []
        poll_sleep_ms = KAFKA_CONFIG.get('poll_sleep_ms', 100)

        for consumer_class in consumer_classes:
            class_name = consumer_class.__name__
            custom_config = consumer_configs.get(class_name, {})
            config = Conf.set_consumer_config(custom_config)
            consumer = consumer_class(config=config)
            consumers.append(consumer)
            logging.info(f"[INFO] Initialized consumer: {class_name}")

        try:
            while True:
                for consumer in consumers:
                    MultiConsumerRunner.check_for_message(consumer)
                time.sleep(poll_sleep_ms / 1000.0)
        except KeyboardInterrupt:
            logging.info("👋 Stopping all consumers...")
        finally:
            for consumer in consumers:
                logging.info(f"🛑 Closing consumer for topic: {consumer.get_topic()}")
                consumer.close()

    @staticmethod
    def check_for_message(consumer):
        msg = consumer.poll(timeout=1.0)
        if msg:
            try:
                consumer.process(msg)
                consumer.commit(msg)
                consumer.on_message_success(msg)
            except Exception as e:
                logging.exception(f"❌ Error processing message from topic {consumer.get_topic()}")
                consumer.on_message_failure(msg, e)
