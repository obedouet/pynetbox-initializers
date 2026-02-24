"""Main initialization script for nb-init."""

import logging
from typing import Optional, List, Dict, Any
from .config import Config
from .connection import NetboxConnection
from .api import NetboxAPI
from .models import Device, IPAddress, VLAN


logger = logging.getLogger(__name__)

class NetboxInitializer:
    """Main class for initializing Netbox with devices, IPs, and VLANs."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize Netbox initializer.
        
        Args:
            config: Config instance
        """
        self.config = config or Config()
        self.config.validate()
        self.connection = NetboxConnection(
            url=self.config.get_url(),
            token=self.config.get_token(),
            username=self.config.get_username(),
            password=self.config.get_password()
            )
        self.api = NetboxAPI(self.connection)
        
    def initialize_devices(self, devices: List[Dict]) -> List[Dict]:
        """Initialize devices in Netbox.
        
        Args:
            devices: List of device dictionaries
            
        Returns:
            List of created devices
        """
        created_devices = []
        for device_data in devices:
            device = self._create_device_with_references(device_data)
            if device:
                created_devices.append(device)
        return created_devices
        
    def _create_device_with_references(self, device_data: Dict) -> Optional[Dict]:
        """Create device and resolve references.
        
        Args:
            device_data: Device data
            
        Returns:
            Created device or None
        """
        # Resolve device type
        device_type_name = device_data.get('device_type')
        device_type = self.api.get_device_type(device_type_name)
        if not device_type:
            logger.error(f"Device type {device_type_name} not found")
            return None
            
        # Resolve device role
        device_role_name = device_data.get('device_role')
        device_role = self.api.get_device_role(device_role_name)
        if not device_role:
            logger.error(f"Device role {device_role_name} not found")
            return None
            
        # Resolve site
        site_name = device_data.get('site')
        site = self.api.get_site(site_name)
        if not site:
            logger.error(f"Site {site_name} not found")
            return None
            
        # Create device
        device_payload = {
            'name': device_data.get('name'),
            'device_type': device_type.id,
            'device_role': device_role.id,
            'site': site.id,
            }
            
        # Add optional fields
        if 'serial' in device_data:
            device_payload['serial'] = device_data['serial']
        if 'asset_tag' in device_data:
            device_payload['asset_tag'] = device_data['asset_tag']
        if 'description' in device_data:
            device_payload['description'] = device_data['description']
            
        return self.api.create_device(device_payload)
        
    def initialize_ip_addresses(self, ips: List[Dict]) -> List[Dict]:
        """Initialize IP addresses in Netbox.
        
        Args:
            ips: List of IP address dictionaries
            
        Returns:
            List of created IP addresses
        """
        created_ips = []
        for ip_data in ips:
            ip = self._create_ip_with_references(ip_data)
            if ip:
                created_ips.append(ip)
        return created_ips
        
    def _create_ip_with_references(self, ip_data: Dict) -> Optional[Dict]:
        """Create IP address and resolve references.
        
        Args:
            ip_data: IP address data
            
        Returns:
            Created IP address or None
        """
        # Resolve device
        device_name = ip_data.get('device')
        device = self.api.get_device(device_name)
        if not device:
            logger.error(f"Device {device_name} not found")
            return None
            
        # Resolve interface
        interface_name = ip_data.get('interface')
        interface = self.api.get_interface(device, interface_name)
        if not interface:
            logger.error(f"Interface {interface_name} not found on device {device_name}")
            return None
        
        # Create IP address
        ip_payload = {
            'address': ip_data.get('address'),
            'device': device.id,
            'interface': interface.id,
            }
            
        # Add optional fields
        if 'description' in ip_data:
            ip_payload['description'] = ip_data['description']
        if 'vrf' in ip_data:
            ip_payload['vrf'] = ip_data['vrf']
        if 'is_primary' in ip_data:
            ip_payload['is_primary'] = ip_data['is_primary']
        return self.api.create_ip_address(ip_payload)
        
    def initialize_vlans(self, vlans: List[Dict]) -> List[Dict]:
        """Initialize VLANs in Netbox.
        
        Args:
            vlans: List of VLAN dictionaries
            
        Returns:
            List of created VLANs
        """
        created_vlans = []
        for vlan_data in vlans:
            vlan = self._create_vlan_with_references(vlan_data)
            if vlan:
                created_vlans.append(vlan)
                return created_vlans
                
    def _create_vlan_with_references(self, vlan_data: Dict) -> Optional[Dict]:
        """Create VLAN and resolve references.
        
        Args:
            vlan_data: VLAN data
            
        Returns:
            Created VLAN or None
        """
        # Create VLAN
        vlan_payload = {
            'vid': vlan_data.get('vid'),
            'name': vlan_data.get('name'),
            }
        
        # Add optional fields
        if 'site' in vlan_data:
            site = self.api.get_site(vlan_data['site'])
            if site:
                vlan_payload['site'] = site.id
        if 'description' in vlan_data:
            vlan_payload['description'] = vlan_data['description']
        if 'tenant' in vlan_data:
            vlan_payload['tenant'] = vlan_data['tenant']
        return self.api.create_vlan(vlan_payload)
