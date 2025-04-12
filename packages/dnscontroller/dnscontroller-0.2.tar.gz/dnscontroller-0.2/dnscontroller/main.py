import os

import click
import yaml
from cloudflare import Cloudflare
from rich.console import Console
from rich.table import Table

console = Console()


def load_config():
    config_path = os.path.expanduser("~/.cfcli.yml")
    if not os.path.exists(config_path):
        raise click.ClickException(
            f"Configuration file not found at {config_path}. Please create it with your Cloudflare credentials."
        )

    with open(config_path) as f:
        config = yaml.safe_load(f)

    if not config.get("defaults", {}).get("token"):
        raise click.ClickException("Cloudflare API token not found in configuration")

    return config["defaults"]


def get_cf_client():
    config = load_config()
    return Cloudflare(api_token=config["token"])


def parse_ttl(ttl_str):
    if ttl_str == "auto":
        return 1
    if ttl_str.endswith("min"):
        return int(ttl_str[:-3]) * 60
    if ttl_str.endswith("h"):
        return int(ttl_str[:-1]) * 3600
    if ttl_str.endswith("d"):
        return int(ttl_str[:-1]) * 86400
    return int(ttl_str)


@click.group()
def main():
    """DNS Controller - Manage DNS records via Cloudflare"""
    pass


@main.command()
@click.argument("domain", required=False)
def ls(domain):
    """List DNS records. If domain is not specified, list all domains."""
    cf = get_cf_client()

    if domain:
        # List records for specific domain
        zones = list(cf.zones.list(name=domain))
        if not zones:
            raise click.ClickException(f"Domain {domain} not found")
        zone_id = zones[0].id
        records = list(cf.dns.records.list(zone_id=zone_id))

        table = Table(title=f"DNS Records for {domain}")
        table.add_column("Type")
        table.add_column("Name")
        table.add_column("Content")
        table.add_column("TTL")

        for record in records:
            table.add_row(record.type, record.name, record.content, str(record.ttl))
    else:
        # List all domains
        zones = list(cf.zones.list())

        table = Table(title="Available Domains")
        table.add_column("Domain")
        table.add_column("Status")

        for zone in zones:
            table.add_row(zone.name, zone.status)

    console.print(table)


@main.command()
@click.argument("record_type")
@click.argument("name")
@click.argument("content")
@click.option("--ttl", default="auto", help="TTL value (e.g. 300, 5min, 1h, 1d, auto)")
@click.option("--proxy/--no-proxy", default=None, help="Enable/disable Cloudflare proxy for this record")
def set(record_type, name, content, ttl, proxy):
    """Set a DNS record."""
    cf = get_cf_client()

    # Extract domain from name and format the record name correctly
    parts = name.split(".")
    if len(parts) < 2:
        raise click.ClickException("Invalid DNS name format")

    domain = ".".join(parts[-2:])
    full_name = name if name.endswith(domain) else f"{name}.{domain}"

    zones = list(cf.zones.list(name=domain))
    if not zones:
        raise click.ClickException(f"Domain {domain} not found")
    zone_id = zones[0].id

    # Check if record exists
    records = list(cf.dns.records.list(zone_id=zone_id, name=full_name, type=record_type))

    data = {"zone_id": zone_id, "type": record_type, "name": full_name, "content": content, "ttl": parse_ttl(ttl)}
    if proxy is not None:
        data["proxied"] = proxy

    if records:
        # Update existing record
        data["dns_record_id"] = records[0].id
        cf.dns.records.update(**data)
        console.print(f"[green]Updated {record_type} record for {full_name}[/green]")
    else:
        # Create new record
        cf.dns.records.create(**data)
        console.print(f"[green]Created {record_type} record for {full_name}[/green]")


@main.command()
@click.argument("record_type")
@click.argument("name")
def rm(record_type, name):
    """Remove a DNS record."""
    cf = get_cf_client()

    # Extract domain from name and format the record name correctly
    parts = name.split(".")
    if len(parts) < 2:
        raise click.ClickException("Invalid DNS name format")

    domain = ".".join(parts[-2:])
    record_name = name if name.endswith(domain) else f"{name}.{domain}"

    zones = list(cf.zones.list(name=domain))
    if not zones:
        raise click.ClickException(f"Domain {domain} not found")
    zone_id = zones[0].id

    # Find and delete record
    records = list(cf.dns.records.list(zone_id=zone_id, name=record_name, type=record_type))

    if not records:
        console.print(f"[red]No {record_type} record found for {record_name}[/red]")
        return

    record_id = records[0].id
    cf.dns.records.delete(zone_id=zone_id, dns_record_id=record_id)
    console.print(f"[green]Deleted {record_type} record for {record_name}[/green]")


if __name__ == "__main__":
    main()
