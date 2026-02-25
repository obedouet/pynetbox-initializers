"""Transformations for entity YAML data to Netbox API format."""

from typing import Dict, Any


class EntityTransformer:
    """Transforms YAML data to match Netbox API requirements."""
    
    def transform(self, entity_name, data)-> Dict[str, Any]:
        """Wrapper to entity method"""
        if hasattr(self, "transform_"+entity_name):
            return getattr(self, "transform_"+entity_name)(data)
        else:
            return None

    @staticmethod
    def transform_custom_fields(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform custom_fields YAML data.
        
        Args:
            data: Raw YAML data
            
        Returns:
            Transformed data for Netbox API
        """
        if 'on_objects' in data:
            data['object_types'] = data.pop('on_objects')
        return data
    
    @staticmethod
    def transform_cables(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform cables YAML data if needed."""
        return data
    
    @staticmethod
    def transform_custom_links(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform custom_links YAML data if needed."""
        return data
    
    @staticmethod
    def transform_tags(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform tags YAML data if needed."""
        return data
    
    @staticmethod
    def transform_config_templates(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform config_templates YAML data if needed."""
        return data
    
    @staticmethod
    def transform_webhooks(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform webhooks YAML data if needed."""
        return data
    
    @staticmethod
    def transform_tenant_groups(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform tenant_groups YAML data if needed."""
        return data
    
    @staticmethod
    def transform_tenants(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform tenants YAML data if needed."""
        return data
    
    @staticmethod
    def transform_site_groups(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform site_groups YAML data if needed."""
        return data
    
    @staticmethod
    def transform_regions(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform regions YAML data if needed."""
        return data
    
    @staticmethod
    def transform_rirs(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform rirs YAML data if needed."""
        return data
    
    @staticmethod
    def transform_asns(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform asns YAML data if needed."""
        return data
    
    @staticmethod
    def transform_sites(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform sites YAML data if needed."""
        return data
    
    @staticmethod
    def transform_locations(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform locations YAML data if needed."""
        return data
    
    @staticmethod
    def transform_rack_roles(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform rack_roles YAML data if needed."""
        return data
    
    @staticmethod
    def transform_racks(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform racks YAML data if needed."""
        return data
    
    @staticmethod
    def transform_power_panels(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform power_panels YAML data if needed."""
        return data
    
    @staticmethod
    def transform_power_feeds(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform power_feeds YAML data if needed."""
        return data
    
    @staticmethod
    def transform_manufacturers(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform manufacturers YAML data if needed."""
        return data
    
    @staticmethod
    def transform_platforms(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform platforms YAML data if needed."""
        return data
    
    @staticmethod
    def transform_device_roles(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform device_roles YAML data if needed."""
        return data
    
    @staticmethod
    def transform_device_types(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform device_types YAML data if needed."""
        return data
    
    @staticmethod
    def transform_cluster_types(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform cluster_types YAML data if needed."""
        return data
    
    @staticmethod
    def transform_cluster_groups(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform cluster_groups YAML data if needed."""
        return data
    
    @staticmethod
    def transform_clusters(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform clusters YAML data if needed."""
        return data
    
    @staticmethod
    def transform_prefix_vlan_roles(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform prefix_vlan_roles YAML data if needed."""
        return data
    
    @staticmethod
    def transform_vlan_groups(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vlan_groups YAML data if needed."""
        return data
    
    @staticmethod
    def transform_vlans(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vlans YAML data if needed."""
        return data
    
    @staticmethod
    def transform_devices(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform devices YAML data if needed."""
        return data
    
    @staticmethod
    def transform_interfaces(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform interfaces YAML data if needed."""
        return data
    
    @staticmethod
    def transform_route_targets(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform route_targets YAML data if needed."""
        return data
    
    @staticmethod
    def transform_vrfs(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vrfs YAML data if needed."""
        return data
    
    @staticmethod
    def transform_aggregates(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform aggregates YAML data if needed."""
        return data
    
    @staticmethod
    def transform_virtual_machines(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform virtual_machines YAML data if needed."""
        return data
    
    @staticmethod
    def transform_virtualization_interfaces(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform virtualization_interfaces YAML data if needed."""
        return data
    
    @staticmethod
    def transform_prefixes(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform prefixes YAML data if needed."""
        return data
    
    @staticmethod
    def transform_ip_addresses(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform ip_addresses YAML data if needed."""
        return data
    
    @staticmethod
    def transform_primary_ips(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform primary_ips YAML data if needed."""
        return data
    
    @staticmethod
    def transform_services(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform services YAML data if needed."""
        return data
    
    @staticmethod
    def transform_service_templates(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform service_templates YAML data if needed."""
        return data
    
    @staticmethod
    def transform_providers(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform providers YAML data if needed."""
        return data
    
    @staticmethod
    def transform_circuit_types(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform circuit_types YAML data if needed."""
        return data
    
    @staticmethod
    def transform_circuits(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform circuits YAML data if needed."""
        return data
    
    @staticmethod
    def transform_config_contexts(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform config_contexts YAML data if needed."""
        return data
    
    @staticmethod
    def transform_contact_groups(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform contact_groups YAML data if needed."""
        return data
    
    @staticmethod
    def transform_contact_roles(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform contact_roles YAML data if needed."""
        return data
    
    @staticmethod
    def transform_contacts(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform contacts YAML data if needed."""
        return data
    
    @classmethod
    def get_transformer(cls, entity_name: str) -> callable:
        """Get the transformation function for a specific entity.
        
        Args:
            entity_name: Name of the entity
            
        Returns:
            Transformation function or default transform method
        """
        transformer_name = f'transform_{entity_name}'
        if hasattr(cls, transformer_name):
            return getattr(cls, transformer_name)
        return cls.transform_custom_fields