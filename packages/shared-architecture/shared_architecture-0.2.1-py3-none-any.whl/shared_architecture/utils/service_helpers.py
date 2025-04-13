import os
import logging
from shared_architecture.connections.timescaledb import TimescaleDBPool
from shared_architecture.connections.redis import RedisConnectionPool
from shared_architecture.connections.rabbitmq import RabbitMQConnection

logging.basicConfig(
    level=os.getenv("LOGGING_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Centralized Connection Manager
class ConnectionManager:
    """
    Manages and provides connections for databases and message queues.
    """
    def __init__(self):
        # Initialize connections as None
        self._timescaledb_pool = None
        self._redis_pool = None
        self._rabbitmq_conn = None

    def initialize(self):
        """
        Initializes all shared connections and pools.
        """
        logging.info("Initializing connection pools and shared services...")

        # Initialize TimescaleDB connection pool
        database_url = self._build_database_url()
        self._timescaledb_pool = TimescaleDBPool(database_url=database_url)

        # Initialize Redis connection pool
        self._redis_pool = RedisConnectionPool()

        # Initialize RabbitMQ connection
        self._rabbitmq_conn = RabbitMQConnection(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            username=os.getenv('RABBITMQ_USER', 'guest'),
            password=os.getenv('RABBITMQ_PASSWORD', 'guest')
        ).connect()

        logging.info("All connections initialized successfully.")

    def _build_database_url(self):
        """
        Builds the TimescaleDB database URL dynamically.
        """
        return f"postgresql://{os.getenv('POSTGRES_USER', 'tradmin')}:" \
               f"{os.getenv('POSTGRES_PASSWORD', 'tradpass')}@" \
               f"{os.getenv('POSTGRES_HOST', 'localhost')}:" \
               f"{os.getenv('POSTGRES_PORT', '5432')}/" \
               f"{os.getenv('POSTGRES_DATABASE', 'timescaledb')}"

    def get_timescaledb_session(self):
        """
        Provides a database session from the TimescaleDB pool.
        """
        if not self._timescaledb_pool:
            raise RuntimeError("TimescaleDB pool has not been initialized.")
        return self._timescaledb_pool.get_session()

    def get_redis_connection(self):
        """
        Provides a Redis connection from the pool.
        """
        if not self._redis_pool:
            raise RuntimeError("Redis pool has not been initialized.")
        return self._redis_pool.get_connection()

    def get_rabbitmq_connection(self):
        """
        Provides the RabbitMQ connection.
        """
        if not self._rabbitmq_conn:
            raise RuntimeError("RabbitMQ connection has not been initialized.")
        return self._rabbitmq_conn

# Singleton instance of ConnectionManager
connection_manager = ConnectionManager()

def initialize_service(service_name: str):
    """
    Initializes the ConnectionManager for shared resources.

    Args:
        service_name (str): The name of the microservice (currently unused, can be extended).
    """
    connection_manager.initialize()
    logging.info(f"Service '{service_name}' initialized.")