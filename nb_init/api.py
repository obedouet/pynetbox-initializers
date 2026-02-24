"""API wrapper for Netbox operations."""
import logging
from typing import Optional, Dict, Any
from .connection import NetboxConnection
from .transformations import EntityTransformer


logger = logging.getLogger(__name__)


class NetboxAPI:
    """Wrapper for Netbox API operations."""
    def __init__(self, connection: NetboxConnection):
        """Initialize Netbox API wrapper.
        
        Args:
            connection: NetboxConnection instance
        """
        self.connection = connection
        self.api = connection.connect()
        self.transformer = EntityTransformer()
        
    def get_device_type(self, name: str) -> Optional[Dict]:
        """Get device type by name.
        
        Args:
            name: Device type name
            
        Returns:
            Device type dictionary or None
        """
        try:
            return self.api.ipam.device_types.get(name=name)
        except Exception as e:
            logger.error(f"Error getting device type {name}: {e}")
            return None
        
    def get_device_role(self, name: str) -> Optional[Dict]:
        """Get device role by name.
        
        Args:
            name: Device role name
            
        Returns:
            Device role dictionary or None
        """
        try:
            return self.api.dcim.device_roles.get(name=name)
        except Exception as e:
            logger.error(f"Error getting device role {name}: {e}")
            return None
    
    def get_site(self, name: str) -> Optional[Dict]:
        """Get site by name.
        
        Args:
            name: Site name
            
        Returns:
            Site dictionary or None
        """
        return self._get_first_by_name('dcim.site', name)
        
    def get_device(self, name: str) -> Optional[Dict]:
        """Get device by name.
        
        Args:
            name: Device name
            
        Returns:
            Device dictionary or None
        """
        return self._get_first_by_name('dcim.device', name)
        
    def get_interface(self, device: Dict, name: str) -> Optional[Dict]:
        """Get interface by name on device.
        
        Args:
            device: Device dictionary
            name: Interface name
            
        Returns:
            Interface dictionary or None
        """
        interfaces = self.api.dcim.interfaces.filter(device_id=device['id'])
        for interface in interfaces:
            if interface['name'] == name:
                return interface
        return None
        
    def _get_first_by_name(self, model: str, name: str) -> Optional[Dict]:
        """Get first item by name from model.
        
        Args:
            model: Netbox model name
            name: Item name
            
        Returns:
            Item dictionary or None
        """
        items = self.api.extras.audit_log.filter(model=model, name=name)
        for item in items:
            return item
        return None
        
    def create_device(self, device_data: Dict) -> Optional[Dict]:
        """Create device.
        
        Args:
            device_data: Device data dictionary
            
        Returns:
            Created device or None
        """
        try:
            transformed_data = self.transformer.transform_devices(device_data)
            device = self.api.dcim.devices.create(**transformed_data)
            logger.info(f"Created device {transformed_data.get('name')}")
            return device
        except Exception as e:
            logger.error(f"Error creating device: {e}")
            return None
            
    def create_ip_address(self, ip_data: Dict) -> Optional[Dict]:
        """Create IP address.
        
        Args:
            ip_data: IP address data dictionary
            
        Returns:
            Created IP address or None
        """
        try:
            transformed_data = self.transformer.transform_ip_addresses(ip_data)
            ip = self.api.ipam.ip_addresses.create(**transformed_data)
            logger.info(f"Created IP address {transformed_data.get('address')}")
            return ip
        except Exception as e:
            logger.error(f"Error creating IP address: {e}")
            return None
            
    def create_vlan(self, vlan_data: Dict) -> Optional[Dict]:
        """Create VLAN in Netbox.
        
        Args:
            vlan_data: VLAN data dictionary
            
        Returns:
            Created VLAN dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_vlans(vlan_data)
            vlan = self.api.ipam.vlans.create(**transformed_data)
            logger.info(f"Created VLAN {transformed_data.get('vid')}")
            return vlan
        except Exception as e:
            logger.error(f"Error creating VLAN: {e}")
            return None
            
    def create_prefix(self, prefix_data: Dict) -> Optional[Dict]:
        """Create prefix in Netbox.
        
        Args:
            prefix_data: Prefix data dictionary
            
        Returns:
            Created prefix dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_prefixes(prefix_data)
            prefix = self.api.ipam.prefixes.create(**transformed_data)
            logger.info(f"Created prefix {transformed_data.get('prefix')}")
            return prefix
        except Exception as e:
            logger.error(f"Error creating prefix: {e}")
            return None
            
    def create_vlan_group(self, vlan_group_data: Dict) -> Optional[Dict]:
        """Create VLAN group in Netbox.
        
        Args:
            vlan_group_data: VLAN group data dictionary
            
        Returns:
            Created VLAN group dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_vlan_groups(vlan_group_data)
            vlan_group = self.api.ipam.vlan_groups.create(**transformed_data)
            logger.info(f"Created VLAN group {transformed_data.get('name')}")
            return vlan_group
        except Exception as e:
            logger.error(f"Error creating VLAN group: {e}")
            return None
            
    def create_prefix_vlan_role(self, prefix_vlan_role_data: Dict) -> Optional[Dict]:
        """Create prefix VLAN role in Netbox.
        
        Args:
            prefix_vlan_role_data: Prefix VLAN role data dictionary
            
        Returns:
            Created prefix VLAN role dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_prefix_vlan_roles(prefix_vlan_role_data)
            prefix_vlan_role = self.api.ipam.prefix_vlan_roles.create(**transformed_data)
            logger.info(f"Created prefix VLAN role {transformed_data.get('name')}")
            return prefix_vlan_role
        except Exception as e:
            logger.error(f"Error creating prefix VLAN role: {e}")
            return None
            
    def create_cluster_type(self, cluster_type_data: Dict) -> Optional[Dict]:
        """Create cluster type in Netbox.
        
        Args:
            cluster_type_data: Cluster type data dictionary
            
        Returns:
            Created cluster type dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_cluster_types(cluster_type_data)
            cluster_type = self.api.virtualization.cluster_types.create(**transformed_data)
            logger.info(f"Created cluster type {transformed_data.get('name')}")
            return cluster_type
        except Exception as e:
            logger.error(f"Error creating cluster type: {e}")
            return None
            
    def create_cluster_group(self, cluster_group_data: Dict) -> Optional[Dict]:
        """Create cluster group in Netbox.
        
        Args:
            cluster_group_data: Cluster group data dictionary
            
        Returns:
            Created cluster group dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_cluster_groups(cluster_group_data)
            cluster_group = self.api.virtualization.cluster_groups.create(**transformed_data)
            logger.info(f"Created cluster group {transformed_data.get('name')}")
            return cluster_group
        except Exception as e:
            logger.error(f"Error creating cluster group: {e}")
            return None
            
    def create_cluster(self, cluster_data: Dict) -> Optional[Dict]:
        """Create cluster in Netbox.
        
        Args:
            cluster_data: Cluster data dictionary
            
        Returns:
            Created cluster dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_clusters(cluster_data)
            cluster = self.api.virtualization.clusters.create(**transformed_data)
            logger.info(f"Created cluster {transformed_data.get('name')}")
            return cluster
        except Exception as e:
            logger.error(f"Error creating cluster: {e}")
            return None
            
    def create_virtual_machine(self, virtual_machine_data: Dict) -> Optional[Dict]:
        """Create virtual machine in Netbox.
        
        Args:
            virtual_machine_data: Virtual machine data dictionary
            
        Returns:
            Created virtual machine dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_virtual_machines(virtual_machine_data)
            virtual_machine = self.api.virtualization.virtual_machines.create(**transformed_data)
            logger.info(f"Created virtual machine {transformed_data.get('name')}")
            return virtual_machine
        except Exception as e:
            logger.error(f"Error creating virtual machine: {e}")
            return None
            
    def create_virtualization_interface(self, virtualization_interface_data: Dict) -> Optional[Dict]:
        """Create virtualization interface in Netbox.
        
        Args:
            virtualization_interface_data: Virtualization interface data dictionary
            
        Returns:
            Created virtualization interface dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_virtualization_interfaces(virtualization_interface_data)
            virtualization_interface = self.api.virtualization.interfaces.create(**transformed_data)
            logger.info(f"Created virtualization interface {transformed_data.get('name')}")
            return virtualization_interface
        except Exception as e:
            logger.error(f"Error creating virtualization interface: {e}")
            return None
            
    def create_asn(self, asn_data: Dict) -> Optional[Dict]:
        """Create ASN in Netbox.
        
        Args:
            asn_data: ASN data dictionary
            
        Returns:
            Created ASN dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_asns(asn_data)
            asn = self.api.ipam.asns.create(**transformed_data)
            logger.info(f"Created ASN {transformed_data.get('asn')}")
            return asn
        except Exception as e:
            logger.error(f"Error creating ASN: {e}")
            return None
            
    def create_rir(self, rir_data: Dict) -> Optional[Dict]:
        """Create RIR in Netbox.
        
        Args:
            rir_data: RIR data dictionary
            
        Returns:
            Created RIR dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_rirs(rir_data)
            rir = self.api.ipam.rirs.create(**transformed_data)
            logger.info(f"Created RIR {transformed_data.get('name')}")
            return rir
        except Exception as e:
            logger.error(f"Error creating RIR: {e}")
            return None
            
    def create_region(self, region_data: Dict) -> Optional[Dict]:
        """Create region in Netbox.
        
        Args:
            region_data: Region data dictionary
            
        Returns:
            Created region dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_regions(region_data)
            region = self.api.dcim.regions.create(**transformed_data)
            logger.info(f"Created region {transformed_data.get('name')}")
            return region
        except Exception as e:
            logger.error(f"Error creating region: {e}")
            return None
            
    def create_site_group(self, site_group_data: Dict) -> Optional[Dict]:
        """Create site group in Netbox.
        
        Args:
            site_group_data: Site group data dictionary
            
        Returns:
            Created site group dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_site_groups(site_group_data)
            site_group = self.api.dcim.site_groups.create(**transformed_data)
            logger.info(f"Created site group {transformed_data.get('name')}")
            return site_group
        except Exception as e:
            logger.error(f"Error creating site group: {e}")
            return None
            
    def create_tenant(self, tenant_data: Dict) -> Optional[Dict]:
        """Create tenant in Netbox.
        
        Args:
            tenant_data: Tenant data dictionary
            
        Returns:
            Created tenant dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_tenants(tenant_data)
            tenant = self.api.dcim.tenants.create(**transformed_data)
            logger.info(f"Created tenant {transformed_data.get('name')}")
            return tenant
        except Exception as e:
            logger.error(f"Error creating tenant: {e}")
            return None
            
    def create_tenant_group(self, tenant_group_data: Dict) -> Optional[Dict]:
        """Create tenant group in Netbox.
        
        Args:
            tenant_group_data: Tenant group data dictionary
            
        Returns:
            Created tenant group dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_tenant_groups(tenant_group_data)
            tenant_group = self.api.dcim.tenant_groups.create(**transformed_data)
            logger.info(f"Created tenant group {transformed_data.get('name')}")
            return tenant_group
        except Exception as e:
            logger.error(f"Error creating tenant group: {e}")
            return None
            
    def create_webhook(self, webhook_data: Dict) -> Optional[Dict]:
        """Create webhook in Netbox.
        
        Args:
            webhook_data: Webhook data dictionary
            
        Returns:
            Created webhook dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_webhooks(webhook_data)
            webhook = self.api.extras.webhooks.create(**transformed_data)
            logger.info(f"Created webhook {transformed_data.get('name')}")
            return webhook
        except Exception as e:
            logger.error(f"Error creating webhook: {e}")
            return None
            
    def create_config_template(self, config_template_data: Dict) -> Optional[Dict]:
        """Create config template in Netbox.
        
        Args:
            config_template_data: Config template data dictionary
            
        Returns:
            Created config template dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_config_templates(config_template_data)
            config_template = self.api.extras.config_templates.create(**transformed_data)
            logger.info(f"Created config template {transformed_data.get('name')}")
            return config_template
        except Exception as e:
            logger.error(f"Error creating config template: {e}")
            return None
            
    def create_custom_link(self, custom_link_data: Dict) -> Optional[Dict]:
        """Create custom link in Netbox.
        
        Args:
            custom_link_data: Custom link data dictionary
            
        Returns:
            Created custom link dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_custom_links(custom_link_data)
            custom_link = self.api.extras.custom_links.create(**transformed_data)
            logger.info(f"Created custom link {transformed_data.get('name')}")
            return custom_link
        except Exception as e:
            logger.error(f"Error creating custom link: {e}")
            return None
            
    def create_cable(self, cable_data: Dict) -> Optional[Dict]:
        """Create cable in Netbox.
        
        Args:
            cable_data: Cable data dictionary
            
        Returns:
            Created cable dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_cables(cable_data)
            cable = self.api.dcim.cables.create(**transformed_data)
            logger.info(f"Created cable {transformed_data.get('name')}")
            return cable
        except Exception as e:
            logger.error(f"Error creating cable: {e}")
            return None
            
    def create_tag(self, tag_data: Dict) -> Optional[Dict]:
        """Create tag in Netbox.
        
        Args:
            tag_data: Tag data dictionary
            
        Returns:
            Created tag dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_tags(tag_data)
            tag = self.api.extras.tags.create(**transformed_data)
            logger.info(f"Created tag {transformed_data.get('name')}")
            return tag
        except Exception as e:
            logger.error(f"Error creating tag: {e}")
            return None
