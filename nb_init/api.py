"""API wrapper for Netbox operations."""
import logging
from typing import Optional, Dict, Any
import pynetbox
from .connection import NetboxConnection
from .transformations import EntityTransformer
from .nb_endpoints import get_endpoint
from .nb_naming import get_unique_name
from .name_template import expand_name_template

logger = logging.getLogger(__name__)


class NetboxAPI:
    """Wrapper for Netbox API operations."""
    def __init__(self, connection: NetboxConnection = None, api: pynetbox.api = None):
        """Initialize Netbox API wrapper.
        
        Args:
            connection: NetboxConnection instance
        """
        self.connection = connection
        if api is None:
            self.api = connection.connect()
        else:
            self.api = api
        self.transformer = EntityTransformer()
        self.primary_ips = []

    def _look_primary_ip_address(self, ip_address):
        """Look for primary ip_address.
        
        Args:
            ip_address: IP Address

        Returns:
            dict(ip_address, device) or None
        """
        for ip in self.primary_ips:
            if ip_address == ip['ip4']:
                return ip
        return None

    def get_device_types(self, name: str)-> Optional[Dict]:
        """Get a device types.

        Args:
            name: model name
        
        Returns:
            Item dictionary or None
        """
        endpoint = get_endpoint(self.api, 'device_types')
        if not endpoint:
            return None
        return endpoint.get(model=name)

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
        return self._get_first_by_name('sites', name)
        
    def get_device(self, name: str) -> Optional[Dict]:
        """Get device by name.
        
        Args:
            name: Device name
            
        Returns:
            Device dictionary or None
        """
        return self.api.dcim.devices.get(name=name)
        
    def get_interface(self, name: str, device: str) -> Optional[Dict]:
        """Get interface by name on device.
        
        Args:
            name: Interface name
            device: Device name
            
        Returns:
            Interface dictionary or None
        """
        interfaces = self.api.dcim.interfaces.filter(name=name, device=device)
        for interface in interfaces:
            if interface['name'] == name:
                return interface
        return None
        
    def get_ip_addresses(self, name: str, device: str)-> Optional[Dict]:
        """Get an ip address.

        Args:
            name: ip address
        
        Returns:
            Item dictionary or None
        """
        endpoint = get_endpoint(self.api, 'ip_addresses')
        if not endpoint:
            return None
        return endpoint.get(address=name, device=device)

    def get_prefixes(self, name: str)-> Optional[Dict]:
        """Get a prefix.

        Args:
            name: prefix
        
        Returns:
            Item dictionary or None
        """
        endpoint = get_endpoint(self.api, 'prefixes')
        if not endpoint:
            return None
        return endpoint.get(prefix=name)

    def _get_first_by_name(self, entity_name, name: str) -> Optional[Dict]:
        """Get item by name.
        
        Args:
            entity_name: Netbox entity
            name: Item name
            
        Returns:
            Item dictionary or None
        """
        endpoint = get_endpoint(self.api, entity_name)
        if not endpoint:
            return None
        return endpoint.get(name=name)
        
    def get_or_create(self, entity_type: str, name: str, data: Dict[str, Any]) -> Optional[Dict]:
        """Get an existing entity or create a new one.
        
        Args:
            entity_type: Type of entity (e.g., 'device_type', 'site', 'vlan')
            name: Name of the entity
            data: Data for creating the entity
            
        Returns:
            The existing or newly created entity, or None if failed
        """
        try:
            # Try to get the entity by name first
            method_name = f"get_{entity_type}"
            
            # Handle entity names that might differ from method names
            # e.g., "virtual_machines" -> "virtual_machine", "device_types" -> "device_type"
            if not hasattr(self, method_name):
                # Try singular form
                singular_name = entity_type
                if entity_type.endswith("s"):
                    singular_name = entity_type[:-1]
                
                # Try common variations
                for suffix in ["_types", "_groups", "_roles", "_feeds", "_types_", "_groups_", "_roles_", "_feeds_"]:
                    if singular_name.endswith(suffix):
                        singular_name = singular_name[:-len(suffix)]
                        break
                
                method_name = f"get_{singular_name}"
            
            # Try to get the entity
            try:
                if 'device' in data:
                    # Get by device
                    entity = getattr(self, method_name)(name, data['device'])
                else:
                    entity = getattr(self, method_name)(name)
                if entity:
                    return entity
            except AttributeError:
                # Retry with generic method
                entity = self._get_first_by_name(entity_type, name)
                if entity:
                    return entity
            except pynetbox.RequestError as e:
                # If entity doesn't exist, this will raise an error, which is expected
                if "Not Found" in str(e):
                    pass
                else:
                    raise
            
            # If we get here, the entity doesn't exist, so create it
            create_method_name = f"create_{entity_type}"
            if not hasattr(self, create_method_name):
                # Try singular form
                singular_name = entity_type
                if entity_type.endswith("s"):
                    singular_name = entity_type[:-1]
                
                for suffix in ["_types", "_groups", "_roles", "_feeds", "_types_", "_groups_", "_roles_", "_feeds_"]:
                    if singular_name.endswith(suffix):
                        singular_name = singular_name[:-len(suffix)]
                        break
                
                create_method_name = f"create_{singular_name}"
            
            # Transform data using the transformer if available
            transformed_data = self.transformer.transform(entity_type, data) if self.transformer else data
            
            # Create the entity
            entity = getattr(self, create_method_name)(transformed_data)
            
            # Return the created entity (includes ID and other fields)
            return entity
            
        except pynetbox.RequestError as e:
            logger.error(f"Error in get_or_create for {entity_type} '{name}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_or_create for {entity_type} '{name}': {e}")
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
            for device_property in ['device_type','role','site','location','rack','config_template','primary_ip4']:
                if device_property in transformed_data:
                    if device_property == 'primary_ip4':
                        # Manage primary ip4 later
                        self.primary_ips.append({'ip4':transformed_data['primary_ip4'],'device':transformed_data.get('name')})
                        transformed_data.pop('primary_ip4')
                        continue
                    else:
                        # Change property to id
                        nb_property = self._get_first_by_name(device_property+'s',name=transformed_data[device_property])
                    if nb_property is None:
                        logger.error(f"Error getting {transformed_data[device_property]} for {transformed_data.get('name')}")
                        return None
                    transformed_data[device_property]=nb_property['id']
            device = self.api.dcim.devices.create(**transformed_data)
            logger.info(f"Created device {transformed_data.get('name')}")
            return device
        except Exception as e:
            logger.error(f"Error creating device: {e}")
            return None

    def create_device_type(self, device_type_data: Dict) -> Optional[Dict]:
        """Create device_type.
        
        Args:
            device_type_data: device_type data dictionary
            
        Returns:
            Created device or None
        """
        try:
            transformed_data = self.transformer.transform_device_types(device_type_data)
            # Check manufacturer
            if 'manufacturer' in transformed_data:
                device_manufacturer=self._get_first_by_name('manufacturers',transformed_data['manufacturer'])
                if device_manufacturer is None:
                    logger.error(f"Error checking manufacturer: {transformed_data['manufacturer']}")
                    return None
                transformed_data['manufacturer']=device_manufacturer['id']
            device = (get_endpoint(self.api, 'device_types')).create(**transformed_data)
            logger.info(f"Created device {transformed_data.get(get_unique_name('device_types', device_type_data))}")
            if 'interfaces' in transformed_data:
                for intf_template in transformed_data['interfaces']:
                    intf_template['device_type']=device['id']
                    if 'name_template' in intf_template:
                        for intf_name in expand_name_template(intf_template['name_template']):
                            intf_template['name']=intf_name
                            self.create_interface_templates(intf_template) 
                    else:
                        self.create_interface_templates(intf_template)
            return device
        except Exception as e:
            logger.error(f"Error creating device_types: {e}")
            return None

    def create_interface_templates(self, interface_data: Dict) -> Optional[Dict]:
        """Create interface_template.
        
        Args:
            interface_data: interface data dictionary
            
        Returns:
            Created interface or None
        """
        try:
            transformed_data = self.transformer.transform_interface_templates(interface_data)
            interface = (get_endpoint(self.api, 'interface_templates')).create(**transformed_data)
            logger.info(f"Created interface {transformed_data.get(get_unique_name('interface_templates', interface_data))}")
            return interface
        except Exception as e:
            logger.error(f"Error creating interface_template: {e}")
            return None

    def create_ip_addresses(self, ip_data: Dict) -> Optional[Dict]:
        """Create IP address.
        
        Args:
            ip_data: IP address data dictionary
            
        Returns:
            Created IP address or None
        """
        try:
            device=None
            transformed_data = self.transformer.transform_ip_addresses(ip_data)
            
            if 'device' in transformed_data:
                # Get device id
                device = self.get_device(transformed_data['device'])
                if device is None:
                    logger.error(f"Error device {transformed_data['device']} for ip_address {transformed_data.get('address')} not found")
                    return None
                transformed_data.pop('device')
            
            if device and 'interface' in transformed_data:
                # Get interface id
                ip_interface = self.get_interface(transformed_data['interface'], device['name'])
                if ip_interface is None:
                    logger.error(f"Error interface {transformed_data['interface']} on {transformed_data['device']} for ip_address {transformed_data.get('address')} not found")
                    return None
                transformed_data.pop('interface')
                transformed_data['assigned_object_id']=ip_interface['id']

            if 'vrf' in transformed_data:
                ip_vrf = self._get_first_by_name('vrfs', transformed_data['vrf'])
                if ip_vrf is None:
                    logger.error(f"Vrf {transformed_data['vrf']} for ip_address {transformed_data.get('address')} not found")
                    return None
                transformed_data['vrf']=ip_vrf['id']
            
            ip = self.api.ipam.ip_addresses.create(**transformed_data)
            logger.info(f"Created IP address {transformed_data.get('address')}")

            is_assigned = self._look_primary_ip_address(transformed_data['address'])
            if is_assigned is not None and device:
                # configure primary ip4
                if device['name']==is_assigned['device']:
                    device['primary_ip4']=ip['id']
                    (get_endpoint(self.api, "devices")).update(device)
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

    def create_custom_field(self, custom_field_data: Dict) -> Optional[Dict]:
        """Create custom field in Netbox.
        
        Args:
            custom_field_data: Custom field data dictionary
            
        Returns:
            Created custom field dictionary or None
        """
        try:
            transformed_data = self.transformer.transform_custom_fields(custom_field_data)
            custom_field = self.api.extras.custom_fields.create(**transformed_data)
            logger.info(f"Created custom field {transformed_data.get('name')}")
            return custom_field
        except Exception as e:
            logger.error(f"Error creating custom field: {e}")
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
