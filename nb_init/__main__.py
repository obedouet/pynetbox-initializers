"""nb-init CLI entry point."""

import argparse
import logging
import sys
from pathlib import Path

from .connection import NetboxConnection
from .config import Config
from .manager import NetboxManager
from .models import Device, IPAddress, VLAN


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Netbox Initializer')
    parser.add_argument('--config', '-c', help='Path to config file')
    parser.add_argument('--url', help='Netbox URL')
    parser.add_argument('--token', help='Netbox API token')
    parser.add_argument('--username', help='Netbox username')
    parser.add_argument('--password', help='Netbox password')
    return parser.parse_args()
    
    
def main():
    args = parse_args()
    
    # Initialize configuration
    config = Config(args.config)
    
    # Create connection
    connection = NetboxConnection(
        url=config.get_url() or args.url,
        token=config.get_token() or args.token,
        username=config.get_username() or args.username,
        password=config.get_password() or args.password
        )
        
    # Create manager
    manager = NetboxManager(connection)
    
    # Example: Create a device
    device = Device(
        name='test-device',
        device_type='Cisco Catalyst 2960',
        role='switch',
        site='Data Center A'
        )
        
    result = manager.create_device(device)
    
    if result:
        print(f"Success! Device created: {result}")
    else:
        print("Failed to create device")
        
    connection.close()
    
    
if __name__ == '__main__':
    main()
    