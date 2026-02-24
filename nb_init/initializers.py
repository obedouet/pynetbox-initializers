"""Entity initializers for Netbox."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import pynetbox


class NetboxInitializer:
    """Handles initialization of Netbox entities from YAML configuration files.
    """
    
    # Entity order - must respect dependencies
    ENTITY_ORDER = [
        "custom_fields",
        "custom_links",
        "tags",
        "config_templates",
        "webhooks",
        "tenant_groups",
        "tenants",
        "site_groups",
        "regions",
        "rirs",
        "asns",
        "sites",
        "locations",
        "rack_roles",
        "racks",
        "power_panels",
        "power_feeds",
        "manufacturers",
        "platforms",
        "device_roles",
        "device_types",
        "cluster_types",
        "cluster_groups",
        "clusters",
        "prefix_vlan_roles",
        "vlan_groups",
        "vlans",
        "devices",
        "interfaces",
        "route_targets",
        "vrfs",
        "aggregates",
        "virtual_machines",
        "virtualization_interfaces",
        "prefixes",
        "ip_addresses",
        "primary_ips",
        "services",
        "service_templates",
        "providers",
        "circuit_types",
        "circuits",
        "cables",
        "config_contexts",
        "contact_groups",
        "contact_roles",
        "contacts"
        ]
    
    def __init__(self, api: pynetbox.api, yaml_dir: str = "yaml"):
        """Initialize the Netbox initializer.
        
        Args:
            api: pynetbox.api instance
            yaml_dir: Directory containing YAML configuration files
        """
        self.api = api
        self.yaml_dir = Path(yaml_dir)
        
    def initialize_all(self):
        """Initialize all entities in the correct order.
        """
        for entity_name in self.ENTITY_ORDER:
            self.initialize_entity(entity_name)
        
    def initialize_entity(self, entity_name: str):
        """Initialize a single entity.
        
        Args:
            entity_name: Name of the entity to initialize
        """
        yaml_file = self.yaml_dir / f"{entity_name}.yml"
        
        if not yaml_file.exists():
            print(f"Warning {entity_name} has no yml file")
            return
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)
            if data and (isinstance(data, dict) or isinstance(data, list)):
                self._process_entity(entity_name, data)
            else:
                print(f"Warning cant proceed for {entity_name}")
    
    def _process_entity(self, entity_name: str, data):
        """Process entity data and create in Netbox.
        
        Args:
            entity_name: Name of the entity
            data: Entity data from YAML
        """
        # Get the appropriate API endpoint
        endpoint = self._get_endpoint(entity_name)
        if not endpoint:
            return
            
        if isinstance(data, dict):
            # Process each item in the entity data
            for item_name, item_data in data.items():
                if isinstance(item_data, dict) and not 'name' in item_data:
                    item_data.update({'name':item_name})
                self._create_item(endpoint, item_name, item_data)
        else:
            for item_data in data:
                if not 'name' in item_data:
                    print(f"Warning missing name in {entity_name}")
                    continue
                self._create_item(endpoint, item_data['name'], item_data)
            
    def _get_endpoint(self, entity_name: str):
        """Get the pynetbox endpoint for an entity.
        
        Args:
            entity_name: Name of the entity
        
        Returns:
            pynetbox endpoint or None
            
        """
        # Map entity names to pynetbox endpoints
        endpoint_map = {
            "custom_fields": self.api.extras.custom_fields,
            "custom_links": self.api.extras.custom_links,
            "tags": self.api.extras.tags,
            "config_templates": self.api.extras.config_templates,
            "webhooks": self.api.extras.webhooks,
            "tenant_groups": self.api.tenancy.tenant_groups,
            "tenants": self.api.tenancy.tenants,
            "site_groups": self.api.dcim.site_groups,
            "regions": self.api.dcim.regions,
            "rirs": self.api.ipam.rirs,
            "asns": self.api.ipam.asns,
            "sites": self.api.dcim.sites,
            "locations": self.api.dcim.locations,
            "rack_roles": self.api.dcim.rack_roles,
            "racks": self.api.dcim.racks,
            "power_panels": self.api.dcim.power_panels,
            "power_feeds": self.api.dcim.power_feeds,
            "manufacturers": self.api.dcim.manufacturers,
            "platforms": self.api.dcim.platforms,
            "device_roles": self.api.dcim.device_roles,
            "device_types": self.api.dcim.device_types,
            "cluster_types": self.api.virtualization.cluster_types,
            "cluster_groups": self.api.virtualization.cluster_groups,
            "clusters": self.api.virtualization.clusters,
            "prefix_vlan_roles": self.api.ipam.prefix_vlan_roles,
            "vlan_groups": self.api.ipam.vlan_groups,
            "vlans": self.api.ipam.vlans,
            "devices": self.api.dcim.devices,
            "interfaces": self.api.dcim.interfaces,
            "route_targets": self.api.ipam.route_targets,
            "vrfs": self.api.ipam.vrfs,
            "aggregates": self.api.ipam.aggregates,
            "virtual_machines": self.api.virtualization.virtual_machines,
            "virtualization_interfaces": self.api.virtualization.interfaces,
            "prefixes": self.api.ipam.prefixes,
            "ip_addresses": self.api.ipam.ip_addresses,
            "primary_ips": self.api.ipam.primary_ips,
            "services": self.api.ipam.services,
            "service_templates": self.api.ipam.service_templates,
            "providers": self.api.circuits.providers,
            "circuit_types": self.api.circuits.circuit_types,
            "circuits": self.api.circuits.circuits,
            "cables": self.api.dcim.cables,
            "config_contexts": self.api.extras.config_contexts,
            "contact_groups": self.api.tenancy.contact_groups,
            "contact_roles": self.api.tenancy.contact_roles,
            "contacts": self.api.tenancy.contacts,
            }
            
        return endpoint_map.get(entity_name)
            
    def _create_item(self, endpoint, item_name: str, item_data: Dict[str, Any]):
        """Create an item in Netbox.
        
        Args:
            endpoint: pynetbox endpoint
            item_name: Name of the item
            item_data: Item data
        """
        try:
            # Check if item already exists
            existing = endpoint.get(name=item_name)
            if existing:
                print(f"Skipped {item_name}: already exists")
                return
                
            # Create the item
            created = endpoint.create(**item_data)
            print(f"Created {item_name}: {item_name}")
        except pynetbox.RequestError as e:
            print(f"Error creating {item_name}: {e}")
        except Exception as e:
            print(f"Unexpected error creating {item_name}: {e}")
