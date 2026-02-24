"""Configuration module for nb-init."""

import os
import yaml
from typing import Optional, Dict, Any
from pathlib import Path

class Config:
    """Handles configuration loading from multiple sources."""
    
    # Environment variable names
    ENV_URL = "NB_URL"
    ENV_USER = "NB_USER"
    ENV_PASSWORD = "NB_PASSWORD"
    
    ENV_TOKEN = "NB_TOKEN"
    
    # Config file name
    CONFIG_FILE = "nb-init.yaml"
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_file: Path to config file (optional)
            
        """
        self.config_file = config_file or self.CONFIG_FILE
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file, environment variables, and defaults.
        
        Returns:
            Dictionary containing configuration
        """
        config = {}
        
        # Load from config file if it exists
        if Path(self.config_file).exists():
            with open(self.config_file, "r") as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    config.update(file_config)

        # Environment variables take priority
        if self.ENV_URL in os.environ:
            config["url"] = os.environ[self.ENV_URL]
        if self.ENV_USER in os.environ:
            config["username"] = os.environ[self.ENV_USER]
        if self.ENV_PASSWORD in os.environ:
            config["password"] = os.environ[self.ENV_PASSWORD]
        if self.ENV_TOKEN in os.environ:
            config["token"] = os.environ[self.ENV_TOKEN]
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def get_url(self) -> Optional[str]:
        return self.get("url")
        
    def get_username(self) -> Optional[str]:
        return self.get("username")
    
    def get_password(self) -> Optional[str]:
        return self.get("password")
        
    def get_token(self) -> Optional[str]:
        return self.get("token")
        
    def has_token(self) -> bool:
        return self.get_token() is not None
        
    def has_credentials(self) -> bool:
        return self.get_username() is not None and self.get_password() is not None
