"""Command-line interface for nb-init."""

import click
from pathlib import Path
from nb_init.connection import NetboxConnection
from nb_init.config import Config
from nb_init.initializers import NetboxInitializer


@click.command()
@click.option("--url", "-u", help="Netbox URL")
@click.option("--username", "-U", help="Netbox username")
@click.option("--password", "-p", help="Netbox password")
@click.option("--token", "-t", help="Netbox API token")
@click.option("--config", "-c", help="Path to config file")
def main(url: str, username: str, password: str, token: str, config: str):
    """Main entry point for nb-init command.
    """
    # Load configuration
    config_obj = Config(config)
    
    # Get values from command line, config file, or environment variables
    # Environment variables take priority
    netbox_url = url or config_obj.get_url()
    netbox_user = username or config_obj.get_username()
    netbox_password = password or config_obj.get_password()
    netbox_token = token or config_obj.get_token()
    
    # Validate required parameters
    if not netbox_url:
        click.echo("Error: Netbox URL is required.", err=True)
        return 1
    
    # Token takes priority over username/password
    if netbox_token:
        click.echo("Using token authentication...")
    elif netbox_user and netbox_password:
        click.echo("Using username/password authentication...")
    else:
        click.echo("Error: Either token or username/password must be provided.", err=True)
        return 1
        
    # Establish connection
    try:
        with NetboxConnection(netbox_url, netbox_token, netbox_user, netbox_password) as nb:
            click.echo("Successfully connected to Netbox!")
            # TODO: Add entity initialization logic here
            NetboxInitializer(nb).initialize_all()
            click.echo("Netbox initialized successfully!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
        
    return 0
    
if __name__ == "__main__":
    main()
