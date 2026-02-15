# Python3 Multivendor Backup
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/AlexMunoz905/Python-Cisco-Backup)

Backup your network configuration of a supported vendor, with easy options for automation.

## Supported Vendors
* Cisco IOS & ASA
* Juniper
* VyOS
* Huawei
* Fortinet
* MicroTik

This is running on Python3 with Netmiko, ping3, Typer, and Loguru.
Version 3.0

## Example:
CLI

![Screenshot of manual option](https://i.imgur.com/46JnIdM.png)
GUI

![Screenshot of GUI option](https://i.imgur.com/bmbiNce.png)

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install netmiko ping3 typer loguru
   ```
3. You need to download this repository or clone it:
   ```bash
   git clone https://github.com/AlexMunoz905/Python-Cisco-Backup.git
   ```

## Usage

### CLI (Command Line Interface)

The CLI uses [Typer](https://typer.tiangolo.com/) for a modern, user-friendly command line experience.

#### Basic Usage

```bash
# Show help
python multivendor_run.py --help

# Run interactive menu (select vendor interactively)
python multivendor_run.py
```

#### Vendor-Specific Commands

```bash
# Backup Cisco IOS devices
python multivendor_run.py cisco-ios

# Backup Cisco ASA devices
python multivendor_run.py cisco-asa

# Backup Juniper devices
python multivendor_run.py juniper

# Backup VyOS routers
python multivendor_run.py vyos

# Backup Huawei devices
python multivendor_run.py huawei

# Backup Fortinet devices
python multivendor_run.py fortinet

# Backup Microtik devices
python multivendor_run.py microtik

# Backup all vendor types
python multivendor_run.py all
```

#### Global Options

```bash
# Use a custom CSV file
python multivendor_run.py cisco-ios --csv /path/to/custom.csv

# Enable verbose/debug logging
python multivendor_run.py cisco-ios --verbose

# Short options
python multivendor_run.py cisco-ios -c custom.csv -v
```

#### CLI Help

Each command has its own help:

```bash
# General help
python multivendor_run.py --help

# Command-specific help
python multivendor_run.py cisco-ios --help
```

### CSV File Format

The CSV file should contain the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| 1 | IP Address/Hostname | Yes |
| 2 | Username | Yes |
| 3 | Password | Yes |
| 4 | Enable Secret | Only for Cisco IOS/ASA |

**Example CSV (`backup_hosts.csv`):**

```csv
192.168.1.1,admin,password123,enable_secret
192.168.1.2,admin,password123
10.0.0.1,root,password456
```

**Note:** The script automatically detects and skips header rows.

### GUI (Graphical User Interface)

1. Download & run executable from GitHub releases tab (if available).
2. Or run the GUI directly:
   ```bash
   python gui.py
   ```
3. Select the vendor you want to copy the config of.
4. Select the CSV file from the popup window.
5. It'll give you a popup for each successful configuration copied, as well as for each down host, if any.

## Settings & Configuration

### Output Directory

Backups are saved to the `backup-config/` directory (created automatically if it doesn't exist).

### Logging

Logs are written to `backup-config/backup.log` with the following features:
- Daily log rotation
- 7-day retention
- Structured format: `YYYY-MM-DD HH:mm:ss | LEVEL | message`

**Log Levels:**
- `INFO` (default) - Standard operation messages
- `DEBUG` (with `--verbose` flag) - Detailed debug information

### Output Files

1. **Configuration backups**: `{hostname}_{MM-DD-YYYY_HH-MM}.txt`
   - Example: `router1_02-15-2026_14-30.txt`

2. **Down devices list**: `down_devices_{MM-DD-YYYY_HH-MM}.txt`
   - Contains IP addresses of unreachable devices

## Getting help

If you are having trouble or need help, create an issue [here](https://github.com/alexmunoz905/Python-Cisco-Backup/issues)

## Contributors
- [ste-giraldo](https://github.com/ste-giraldo) for adding a memory and CPU saving feature to grabbing the hostname, and suggesting the ping feature.

## Credits and references

- [Netmiko](https://github.com/ktbyers/netmiko) by Kirk Byers
- [Ping3](https://github.com/kyan001/ping3) by Kyan
- [Typer](https://github.com/tiangolo/typer) by Sebastián Ramírez
- [Loguru](https://github.com/Delgan/loguru) by Delgan

----

## Licensing info

This code is with the MIT license.
