# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_pubsub', 'kafka_pubsub.config']

package_data = \
{'': ['*']}

install_requires = \
['confluent-kafka>=2.3.0,<3.0.0', 'python-dotenv>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'kafka-pubsub',
    'version': '0.2.1',
    'description': 'Kafka pub/sub utilities',
    'long_description': 'Apache Kafka customized Producer, Consumer, helper classes and methods',
    'author': 'Emmanuel Chukwu',
    'author_email': 'emmanuel.chukwu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
