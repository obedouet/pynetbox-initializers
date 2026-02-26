"""Get Netbox API endpoint from entity name"""

def get_endpoint(api, entity_name: str):
    """Get the pynetbox endpoint for an entity.
    
    Args:
        entity_name: Name of the entity
    
    Returns:
        pynetbox endpoint or None
        
    """
    # Map entity names to pynetbox endpoints
    endpoint_map = {
        "custom_fields": api.extras.custom_fields,
        "custom_links": api.extras.custom_links,
        "tags": api.extras.tags,
        "config_templates": api.extras.config_templates,
        "webhooks": api.extras.webhooks,
        "tenant_groups": api.tenancy.tenant_groups,
        "tenants": api.tenancy.tenants,
        "site_groups": api.dcim.site_groups,
        "regions": api.dcim.regions,
        "rirs": api.ipam.rirs,
        "asns": api.ipam.asns,
        "sites": api.dcim.sites,
        "locations": api.dcim.locations,
        "rack_roles": api.dcim.rack_roles,
        "racks": api.dcim.racks,
        "power_panels": api.dcim.power_panels,
        "power_feeds": api.dcim.power_feeds,
        "manufacturers": api.dcim.manufacturers,
        "platforms": api.dcim.platforms,
        "device_roles": api.dcim.device_roles,
        "device_types": api.dcim.device_types,
        "cluster_types": api.virtualization.cluster_types,
        "cluster_groups": api.virtualization.cluster_groups,
        "clusters": api.virtualization.clusters,
        "prefix_vlan_roles": api.ipam.roles,
        "vlan_groups": api.ipam.vlan_groups,
        "vlans": api.ipam.vlans,
        "devices": api.dcim.devices,
        "interfaces": api.dcim.interfaces,
        "route_targets": api.ipam.route_targets,
        "vrfs": api.ipam.vrfs,
        "aggregates": api.ipam.aggregates,
        "virtual_machines": api.virtualization.virtual_machines,
        "virtualization_interfaces": api.virtualization.interfaces,
        "prefixes": api.ipam.prefixes,
        "ip_addresses": api.ipam.ip_addresses,
        "primary_ips": api.ipam.primary_ips,
        "services": api.ipam.services,
        "service_templates": api.ipam.service_templates,
        "providers": api.circuits.providers,
        "circuit_types": api.circuits.circuit_types,
        "circuits": api.circuits.circuits,
        "cables": api.dcim.cables,
        "config_contexts": api.extras.config_contexts,
        "contact_groups": api.tenancy.contact_groups,
        "contact_roles": api.tenancy.contact_roles,
        "contacts": api.tenancy.contacts,
        "interface_templates": api.dcim.interface_templates
        }
        
    return endpoint_map.get(entity_name)
