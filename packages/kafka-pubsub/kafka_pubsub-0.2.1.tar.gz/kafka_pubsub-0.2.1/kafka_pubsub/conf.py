# kafka_lib/conf.py

from kafka_pubsub.config.pubsub import KAFKA_CONFIG

class Conf:

    @staticmethod
    def merge_config(overrides: dict = None) -> dict:
        config = KAFKA_CONFIG.copy()
        if overrides:
            config.update(overrides)
        return config

    @staticmethod
    def set_common_parameters(overrides: dict = None) -> dict:
        merged = Conf.merge_config(overrides)

        config = {
            'bootstrap.servers': merged['bootstrap_servers'],
            'security.protocol': merged.get('security_protocol') or 'PLAINTEXT',
        }

        if config['security.protocol'] == 'SASL_SSL':
            config.update({
                'sasl.mechanisms': merged['sasl_mechanisms'],
                'sasl.username': merged['sasl_username'],
                'sasl.password': merged['sasl_password'],
            })
        
        # Optional debug settings (e.g., from env: KAFKA_DEBUG=all)
        if merged.get('debug'):
            config['debug'] = merged['debug']

        return config

    @staticmethod
    def set_producer_config(overrides: dict = None) -> dict:
        merged = Conf.merge_config(overrides)
        config = Conf.set_common_parameters(merged)
        config['message.send.max.retries'] = str(merged.get('message_send_max_retries', 5))
        return config

    @staticmethod
    def set_consumer_config(overrides: dict = None) -> dict:
        merged = Conf.merge_config(overrides)
        config = Conf.set_common_parameters(merged)

        config['group.id'] = merged['consumer_group']
        config['auto.offset.reset'] = merged.get('auto_offset_reset', 'earliest')
        config['enable.auto.commit'] = merged.get('enable_auto_commit', False)
        config['max.poll.interval.ms'] = str(merged.get('max_poll_interval_ms', 90000))

        return config

    @staticmethod
    def get_topic_conf():
        return {
            'message.timeout.ms': '30000',
            'request.required.acks': '-1',
            'request.timeout.ms': '5000'
        }
