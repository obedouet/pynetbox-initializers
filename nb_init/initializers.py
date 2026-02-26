"""Entity initializers for Netbox."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import pynetbox

from nb_init.api import NetboxAPI


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
        self.nb_api = NetboxAPI(api=api)
        
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
            
        if isinstance(data, dict):
            # Process each item in the entity data
            for item_name, item_data in data.items():
                if isinstance(item_data, dict) and not 'name' in item_data:
                    item_data.update({'name':item_name})
                self._create_item(entity_name, item_name, item_data)
        else:
            for item_data in data:
                if not 'name' in item_data:
                    print(f"Warning missing name in {entity_name}")
                    continue
                self._create_item(entity_name, item_data['name'], item_data)
                        
    def _create_item(self, entity_name, item_name: str, item_data: Dict[str, Any]):
        """Create or get an item in Netbox.

        Args:
            endpoint: pynetbox endpoint
            item_name: Name of the item
            item_data: Item data
        """
        try:
            # Use the new get_or_create method from NetboxApi
            # Note: We need to determine the entity type from the endpoint
            # For now, we'll assume item_data has the necessary structure
            # or we'll call the method differently

            # Call get_or_create with the data
            result = self.nb_api.get_or_create(entity_name, item_name, item_data)
            if result:
                print(f"{'Got' if result else 'Created'} {item_name}")
            else:
                print(f"Error processing {item_name}")

        except pynetbox.RequestError as e:
            print(f"Error processing {item_name}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {item_name}: {e}")
