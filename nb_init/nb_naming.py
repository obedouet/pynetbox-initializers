"""Helper to find the unique name of an object instance"""

from typing import Dict, Any

ENTITY_UNIQUE_NAME = {
        "asns": "asn",
        "ip_addresses":"address",
        "device_types":"model"
    }

def get_unique_name(entity_name: str, item_data: Dict[str, Any]) -> str:
    """Get the unique name of the item.
    
    Args:
        entity_name: netbox model name
        item_data: Item data

    Returns:
        str: value to use as unique name
    """
    if entity_name in ENTITY_UNIQUE_NAME and ENTITY_UNIQUE_NAME[entity_name] in item_data:
        return ENTITY_UNIQUE_NAME[entity_name]
    return None
