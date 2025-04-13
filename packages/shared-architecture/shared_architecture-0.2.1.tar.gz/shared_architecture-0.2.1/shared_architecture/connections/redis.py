"""
Redis Connection Module

This module provides functionality to manage connections to Redis
using connection pooling for improved performance and scalability.
"""

import os
from redis import Redis, ConnectionPool

class RedisConnectionPool:
    def __init__(self):
        self.pool = ConnectionPool(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            max_connections=10
        )

    def get_connection(self):
        """
        Retrieve a Redis connection using the connection pool.

        Returns:
            Redis: Redis connection instance.
        """
        return Redis(connection_pool=self.pool)