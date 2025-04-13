"""
Config Manager Module

This module provides functionality to manage service-specific configurations,
retrieve them dynamically, and handle loading from environment variables,
ConfigMaps, or Secrets.

Classes:
    - ConfigManager: Manages configuration retrieval for services.
"""

import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class ConfigManager:
    """
    Manages service-specific configuration retrieval.

    This class dynamically loads configurations using environment variables,
    ConfigMaps, or Secrets, providing a centralized interface for configuration
    management across services.
    """

    def __init__(self, service_name: str, config_data: dict = None):
        """
        Initialize ConfigManager with the service name and optional configuration data.

        Args:
            service_name (str): The name of the service.
            config_data (dict, optional): A dictionary containing initial configurations.
        """
        self.service_name = service_name
        self.config_data = config_data or self.load_config()

    def get_service_configs(self) -> dict:
        """
        Retrieve service-specific configurations.

        Returns:
            dict: A dictionary of service configurations.
        """
        service_configs = self.config_data.get("services", {}).get(self.service_name, {})
        if not service_configs:
            logging.warning("No specific configurations found for service '%s'", self.service_name)
        return service_configs

    def load_config(self) -> dict:
        """
        Load the service-specific configuration from environment variables.

        Returns:
            dict: Configuration data loaded from the environment.
        """
        config_data = {
            "POSTGRES_USER": os.getenv("POSTGRES_USER", "traduser"),
            "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", "tradpass"),
            "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "5432"),
            "POSTGRES_DATABASE": os.getenv("POSTGRES_DATABASE", "timescaledb"),
            "RABBITMQ_URL": os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
            "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
            "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
        }
        logging.info(
            "Configurations for %s loaded successfully: %s",
            self.service_name,
            config_data,
        )
        return {"services": {self.service_name: config_data}}

    def handle_error(self, error: Exception):
        """
        Handle errors gracefully.

        Args:
            error (Exception): The exception to log.
        """
        logging.error("Error loading configuration for service '%s': %s", self.service_name, error)