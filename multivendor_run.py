"""
Multi-vendor network device backup script with CLI and GUI support.

This module can be used both as a CLI tool (with typer) and as a library
for the GUI interface in gui.py.
"""

from csv import reader
from datetime import datetime
from ping3 import ping
from vendor_backups import (
    cisco_ios,
    cisco_asa,
    fortinet,
    huawei,
    juniper,
    microtik,
    vyos,
)
import os
import sys
from typing import Optional
from loguru import logger
import typer

# Configure loguru logging
logger.remove()  # Remove default handler
logger.add(
    "backup-config/backup.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)
logger.add(sys.stderr, format="{level}: {message}", level="INFO")

# CSV file for the script to grab the hosts from
CSV_NAME = "backup_hosts.csv"

# Vendor mapping: key is the selection string, value is (module, needs_secret)
VENDOR_MAP = {
    "1": (cisco_ios, True),
    "2": (cisco_asa, True),
    "3": (juniper, False),
    "4": (vyos, False),
    "5": (huawei, False),
    "6": (fortinet, False),
    "7": (microtik, False),
}

# Vendor names for display
VENDOR_NAMES = {
    "1": "Cisco IOS",
    "2": "Cisco ASA",
    "3": "Juniper",
    "4": "VyOS",
    "5": "Huawei",
    "6": "Fortinet",
    "7": "Microtik",
}


def get_timestamp() -> str:
    """Get current timestamp formatted as MM-DD-YYYY_HH-MM."""
    now = datetime.now()
    return now.strftime("%m-%d-%Y_%H-%M")


def ensure_backup_dir():
    """Ensure the backup-config directory exists."""
    if not os.path.exists("backup-config"):
        os.makedirs("backup-config")
        logger.info("Created backup-config directory")


def run_script(
    user_selection: str, csv_file: Optional[str] = None, interactive: bool = False
) -> dict:
    """
    Main backup function that processes devices from CSV.

    Args:
        user_selection: Vendor selection ("1"-"7")
        csv_file: Path to CSV file (defaults to CSV_NAME constant)
        interactive: Whether to show interactive prompts

    Returns:
        dict with results: {'success': int, 'failed': int, 'down': int, 'files': list}
    """
    ensure_backup_dir()
    dt_string = get_timestamp()

    csv_path = csv_file or CSV_NAME

    if user_selection not in VENDOR_MAP:
        logger.error(f"Invalid vendor selection: {user_selection}")
        raise ValueError(f"Invalid vendor selection: {user_selection}")

    vendor_module, needs_secret = VENDOR_MAP[user_selection]
    vendor_name = VENDOR_NAMES[user_selection]

    logger.info(f"Starting backup for {vendor_name} devices from {csv_path}")

    results = {"success": 0, "failed": 0, "down": 0, "files": [], "down_devices": []}

    try:
        with open(csv_path, "r") as read_obj:
            csv_reader = reader(read_obj)
            list_of_rows = list(csv_reader)

            # Skip header row if present
            if len(list_of_rows) > 0:
                # Check if first row contains headers (no IP address)
                first_row = list_of_rows[0]
                try:
                    # Try to parse first element as IP to detect if it's a header
                    import ipaddress

                    ipaddress.ip_address(first_row[0])
                    data_rows = list_of_rows
                except ValueError:
                    # First row is likely a header, skip it
                    data_rows = list_of_rows[1:] if len(list_of_rows) > 1 else []
            else:
                data_rows = []

            total_rows = len(data_rows)
            logger.info(f"Found {total_rows} devices to process")

            for row in data_rows:
                if len(row) < 3:
                    logger.warning(f"Skipping malformed row: {row}")
                    continue

                ip = row[0]
                username = row[1]
                password = row[2]
                secret = row[3] if len(row) > 3 and needs_secret else None

                # Ping the host
                ip_ping = ping(ip, timeout=2)

                if ip_ping is None or ip_ping is False:
                    # Device is down
                    down_file = f"down_devices_{dt_string}.txt"
                    with open(f"backup-config/{down_file}", "a") as f:
                        f.write(f"{ip}\n")

                    logger.warning(f"Device {ip} is down")
                    results["down"] += 1
                    results["down_devices"].append(ip)

                    if interactive:
                        print(f"{ip} is down!")
                else:
                    # Device is up, attempt backup
                    try:
                        logger.info(f"Backing up {ip} ({vendor_name})")

                        if needs_secret and secret:
                            vendor_module.backup(ip, username, password, secret)
                        else:
                            vendor_module.backup(ip, username, password)

                        results["success"] += 1
                        logger.success(f"Successfully backed up {ip}")

                    except Exception as e:
                        results["failed"] += 1
                        logger.error(f"Failed to backup {ip}: {e}")

                        if interactive:
                            print(f"Error backing up {ip}: {e}")

    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during backup: {e}")
        raise

    logger.info(
        f"Backup complete: {results['success']} succeeded, "
        f"{results['failed']} failed, {results['down']} down"
    )

    return results


# Typer CLI app
app = typer.Typer(help="Multi-vendor network device backup tool", no_args_is_help=True)


@app.callback()
def main(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file with device list"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
):
    """Network device backup tool supporting multiple vendors."""
    if verbose:
        logger.remove()
        logger.add(sys.stderr, format="{level}: {message}", level="DEBUG")
        logger.add(
            "backup-config/backup.log",
            rotation="1 day",
            retention="7 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="DEBUG",
        )


@app.command(name="all")
def backup_all(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup all vendor types from the CSV."""
    logger.info("Starting backup for all vendors")

    for selection in VENDOR_MAP.keys():
        try:
            results = run_script(selection, csv_file)
            logger.info(f"{VENDOR_NAMES[selection]}: {results['success']} succeeded")
        except Exception as e:
            logger.error(f"Error backing up {VENDOR_NAMES[selection]}: {e}")


@app.command(name="cisco-ios")
def backup_cisco_ios(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Cisco IOS devices."""
    results = run_script("1", csv_file, interactive=True)
    typer.echo(f"Cisco IOS backup complete: {results['success']} succeeded")


@app.command(name="cisco-asa")
def backup_cisco_asa(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Cisco ASA devices."""
    results = run_script("2", csv_file, interactive=True)
    typer.echo(f"Cisco ASA backup complete: {results['success']} succeeded")


@app.command(name="juniper")
def backup_juniper(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Juniper devices."""
    results = run_script("3", csv_file, interactive=True)
    typer.echo(f"Juniper backup complete: {results['success']} succeeded")


@app.command(name="vyos")
def backup_vyos(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup VyOS routers."""
    results = run_script("4", csv_file, interactive=True)
    typer.echo(f"VyOS backup complete: {results['success']} succeeded")


@app.command(name="huawei")
def backup_huawei(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Huawei devices."""
    results = run_script("5", csv_file, interactive=True)
    typer.echo(f"Huawei backup complete: {results['success']} succeeded")


@app.command(name="fortinet")
def backup_fortinet(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Fortinet devices."""
    results = run_script("6", csv_file, interactive=True)
    typer.echo(f"Fortinet backup complete: {results['success']} succeeded")


@app.command(name="microtik")
def backup_microtik(
    csv_file: Optional[str] = typer.Option(
        None, "--csv", "-c", help="Path to CSV file"
    ),
):
    """Backup Microtik devices."""
    results = run_script("7", csv_file, interactive=True)
    typer.echo(f"Microtik backup complete: {results['success']} succeeded")


# Interactive menu (for backward compatibility when run directly)
def interactive_menu():
    """Show interactive menu for vendor selection."""
    print("\nMulti-Vendor Network Backup Tool")
    print("=" * 40)

    for key, name in VENDOR_NAMES.items():
        print(f"{key}. Backup {name} devices")

    print()
    user_selection = input("Please pick an option: ")

    if user_selection in VENDOR_MAP:
        try:
            results = run_script(user_selection, interactive=True)
            print(f"\nBackup complete!")
            print(f"  Success: {results['success']}")
            print(f"  Failed: {results['failed']}")
            print(f"  Down: {results['down']}")
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            print(f"Error: {e}")
    else:
        print("Invalid option selected")


if __name__ == "__main__":
    # Check if running with arguments (CLI mode) or without (interactive mode)
    if len(sys.argv) > 1:
        app()
    else:
        interactive_menu()
