"""Netbox models and data structures."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Device:
    """Represents a Netbox device.
    """
    name: str
    device_type: str
    role: str
    site: str
    manufacturer: Optional[str] = None
    platform: Optional[str] = None
    serial: Optional[str] = None
    asset_tag: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        """
        return {
            "name": self.name,
            "device_type": self.device_type,
            "role": self.role,
            "site": self.site,
            "manufacturer": self.manufacturer,
            "platform": self.platform,
            "serial": self.serial,
            "asset_tag": self.asset_tag,
            "description": self.description
        }
        
        
@dataclass
class IPAddress:
    """Represents an IP address.
    """
    address: str
    device: str
    interface: str
    vrf: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        """
        return {
            "address": self.address,
            "device": self.device,
            "interface": self.interface,
            "vrf": self.vrf,
            "description": self.description
            }
            
            
@dataclass
class VLAN:
    """Represents a VLAN.
    """
    vid: int
    name: str
    site: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        """
        return {
            "vid": self.vid,
            "name": self.name,
            "site": self.site,
            "description": self.description
            }
