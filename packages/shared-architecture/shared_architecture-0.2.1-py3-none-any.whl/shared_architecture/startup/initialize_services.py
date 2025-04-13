import pika
import logging
from shared_architecture.config import shared_config
from shared_architecture.utils import get_common_config
from shared_architecture.utils import get_scoped_config
def connect_rabbitmq():
    try:
        config_map_data = shared_config.fetch_config()
        logging.info("Connecting to RabbitMQ...")
        parameters = pika.URLParameters(config_map_data.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"))
        connection = pika.BlockingConnection(parameters)
        logging.info("RabbitMQ connection established")
        return connection
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        raise RuntimeError("Unable to connect to RabbitMQ")
