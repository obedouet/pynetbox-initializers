"""Netbox manager for creating and managing objects."""

import logging
from typing import List, Optional
from .connection import NetboxConnection
from .models import Device, IPAddress, VLAN


logger = logging.getLogger(__name__)


class NetboxManager:
    """Manages Netbox API operations."""
    
    def __init__(self, connection: NetboxConnection):
        """Initialize manager.
        
        Args:
            connection: NetboxConnection instance
        """
        self.connection = connection
        
    def create_device(self, device: Device) -> Optional[Dict]:
        """Create a device in Netbox.
        
        Args:
            device: Device object
            
        Returns:
            Created device data or None if failed
        """
        try:
            api = self.connection.connect()
            device_data = device.to_dict()
            created = api.dcim.devices.create(**device_data)
            logger.info(f"Created device: {created}")
            return created
        except Exception as e:
            logger.error(f"Failed to create device: {e}")
            return None
            
    def create_ip_address(self, ip: IPAddress) -> Optional[Dict]:
        """Create an IP address in Netbox.
        
        Args:
            ip: IPAddress object
            
        Returns:
            Created IP address data or None if failed
        """
        try:
            api = self.connection.connect()
            ip_data = ip.to_dict()
            created = ip.ipam.ip_addresses.create(**ip_data)
            logger.info(f"Created IP address: {created}")
            return created
        except Exception as e:
            logger.error(f"Failed to create IP address: {e}")
            return None
            
    def create_vlan(self, vlan: VLAN) -> Optional[Dict]:
        """Create a VLAN in Netbox.
        
        Args:
            vlan: VLAN object
            
        Returns:
            Created VLAN data or None if failed
            
        """
        try:
            api = self.connection.connect()
            vlan_data = vlan.to_dict()
            created = api.ipam.vlans.create(**vlan_data)
            logger.info(f"Created VLAN: {created}")
            return created
        except Exception as e:
            logger.error(f"Failed to create VLAN: {e}")
            return None
            
    def get_device_type(self, name: str) -> Optional[Dict]:
        """Get device type by name.
        
        Args:
            name: Device type name
            
        Returns:
            Device type data or None
        """
        try:
            api = self.connection.connect()
            device_type = api.dcim.device_types.get(name=name)
            return device_type
        except Exception as e:
            logger.error(f"Failed to get device type: {e}")
            return None
            
    def get_site(self, name: str) -> Optional[Dict]:
        """Get site by name.
        
        Args:
            name: Site name
            
        Returns:
            Site data or None
        """
        try:
            api = self.connection.connect()
            site = api.dcim.sites.get(name=name)
            return site
        except Exception as e:
            logger.error(f"Failed to get site: {e}")
            return None
