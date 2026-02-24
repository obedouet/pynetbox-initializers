"""Connection module for Netbox API."""

import os
from typing import Optional
import pynetbox


class NetboxConnection:
    """Handles Netbox API connection."""
    
    def __init__(self, url: str, token: Optional[str] = None, 
                 username: Optional[str] = None, password: Optional[str] = None):
        """Initialize Netbox connection.
        
        Args:
            url: Netbox URL
            token: Netbox API token (takes priority over username/password)
            username: Netbox username
            password: Netbox password
        """
        self.url = url
        self.token = token
        self.username = username
        self.password = password
        self.api = None
        self._token_created = False
    
    def connect(self) -> pynetbox.api:
        """Establish connection to Netbox.
    
        Returns:
            pynetbox.api instance

        Raises:
            ValueError: If neither token nor credentials are provided
        """
        if self.token:
            # Use token authentication
            self.api = pynetbox.api(self.url, token=self.token)
        elif self.username and self.password:
            # Use username/password authentication
            self.api = pynetbox.api(self.url)
            self._token_created = True
            self.token = self.api.create_token(self.username, self.password)
        else:
            raise ValueError(
                "Either token or username/password must be provided. "
                "Token takes priority over username/password."
                    )
        return self.api
        
    def close(self):
        """Close the connection."""
        if self._token_created and self.token:
            # Delete the created token
            try:
                self.api.token.delete()
            except Exception:\
                pass
            self.api = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
