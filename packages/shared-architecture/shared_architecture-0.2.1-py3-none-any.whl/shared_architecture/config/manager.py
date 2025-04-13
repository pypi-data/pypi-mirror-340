import os
import logging
from typing import Dict

class ConfigManager:
    def __init__(self, service_name: str = None):
        """
        Initialize the ConfigManager with the service name.
        Args:
            service_name (str): Name of the service. If None, it is auto-detected.
        """
        self.service_name = service_name or os.getenv("SERVICE_NAME", "default-service")
        self.namespace = os.getenv("NAMESPACE", "default")
        self.configmap_name = os.getenv("CONFIGMAP_NAME", "shared-config")

    def get_env(self, key: str, default: str = None) -> str:
        """
        Retrieve environment variables with a fallback to a default value.
        Args:
            key (str): Environment variable key.
            default (str): Default value if the key is not found.
        Returns:
            str: Value of the environment variable or default.
        """
        value = os.getenv(key, default)
        if value is None:
            logging.warning(f"Environment variable '{key}' not found. Using default: {default}")
        return value

    def get_service_configs(self) -> Dict[str, str]:
        """
        Retrieve all accessible configurations for the service.
        Returns:
            Dict[str, str]: Combined configuration dictionary.
        """
        shared_configs = {key: self.get_env(key) for key in os.environ if key.startswith("SHARED_")}
        scoped_configs = {key: self.get_env(key) for key in os.environ if key.startswith(self.service_name.upper())}
        private_configs = {key: self.get_env(key) for key in os.environ if key.startswith("PRIVATE_")}
        
        # Combine configs with priority: private > scoped > shared
        return {**shared_configs, **scoped_configs, **private_configs}