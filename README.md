# pynetbox-initializers

This is a replacement project for https://github.com/tobiasge/netbox-initializers/ by using pynetbox instead of netbox plugin architecture.

It avoid to be dependant on netbox internal database scheme and it providing information when a problem occur at object creation.

## Installation

```
python3 setup.py dist
pip install dist/<version>.tar.gz
```

## Usage

Usage is very simple:

```
Usage: nb-init [OPTIONS]

  Main entry point for nb-init command.

Options:
  -u, --url TEXT       Netbox URL
  -U, --username TEXT  Netbox username
  -p, --password TEXT  Netbox password
  -t, --token TEXT     Netbox API token
  -c, --config TEXT    Path to config file
```

Netbox URL, username, password or token can also be provided from environment variables:
* NB_URL
* NB_USER
* NB_PASSWORD  
* NB_TOKEN

The default config file is "nb-init.yaml".

nb-init will look for a "yaml" directory and will proceed for each ".yml" file located in. Files must respect the input for netbox-initializers, same naming, same format.
nb-init will check and push through Netbox API using pynetbox.
