# minakicoin/cli/list.py
import click
from minakicoin.services.wallet_store import list_wallets

@click.command("list")
def list_wallets():
    """List all wallets"""
    wallets = list_wallets()
    if not wallets:
        click.echo("No wallets found.")
    else:
        for w in wallets:
            click.echo(f"🔖 {w['label']} - {w['address']}")
