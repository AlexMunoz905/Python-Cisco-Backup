# Python3 Multivendor Backup
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/AlexMunoz905/Python-Cisco-Backup)

Backup your network configuration of a supported vendor, with easy options for automation.
#### Supported Vendors
* Cisco
* Juniper
* VyOS
* Huawei
* Fortinet
* MicroTik

This is running on Python3 with Netmiko, and ping3.
Version 2.1

## Example:
CLI
![Screenshot of manual option](https://i.imgur.com/xLFbP88.png)
GUI
![Screenshot of manual option](https://i.imgur.com/5zjspAp.png)

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on.
2. You need to run `pip3 install netmiko` or `pip install netmiko` in a command prompt / terminal on your computer.
3. You need to run `pip3 install ping3` or `pip install ping3` in a command prompt / terminal on your computer.
4. You need to download this repository or copy all of the contents of the run.py file into a python file.

## Usage of this program
#### CLI
1. To run this, you need to run `python3 multivendor_run.py`  in your terminal or command prompt.
2. Host list will be taken from `backup_hosts.csv`. Please populate the file with the host, username, password, with **optional** secret for cisco devices.
3. It will copy the saved configuration into a folder named `backup-config` in the same directory of the python file. The configuration file name will be the Cisco device hostname, date, and time. Unreachable hosts will be listed in a separated file named `downDevices_` + date and time.

#### GUI
1. Download & run executable from GitHub releases tab.
2. Select the vendor you want to copy the config of.
3. Select the CSV file from the popup window.
4. It'll give you a popup for each successfull configuration copied, as well as for each down host, if any.

## Getting help

If you are having trouble or need help, create an issue [here](https://github.com/alexmunoz905/Python-Cisco-Backup/issues)

## Contributors
[ste-giraldo](https://github.com/ste-giraldo) for adding a memory and cpu saving feature to grabbing the hostname, and suggesting the ping feature.

## Credits and references

I'd like to credit Kirk Byers for making [Netmiko](https://github.com/ktbyers/netmiko), and Kyan for making [Ping3](https://github.com/kyan001/ping3)

----

## Licensing info

This code is with the MIT license.
