# Python3 Multivendor Backup
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/AlexMunoz905/Python-Cisco-Backup)

Backup your saved Cisco configuration from your device to a folder with the hostname, date, and time. You have the option of having it all imported from a CSV file, or manually giving it the IP, Username, Password, and Enable Secret of each host.

This is running on Python3 with Netmiko, and ping3.
Version 2.0



Manual Option:

![Screenshot of manual option](https://i.imgur.com/7SyRGe6.png)


CSV Option:

![Screenshot of CSV option](https://i.imgur.com/NOuNLoB.png)


## Use case of this program

The use case is that you are needing a backup of the saved configuration on your routers or switches.

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on.
2. You need to run `pip3 install netmiko` or `pip install netmiko` in a command prompt / terminal on your computer.
3. You need to run `pip3 install ping3` or `pip install ping3` in a command prompt / terminal on your computer.
4. You need to download this repository or copy all of the contents of the run.py file into a python file.

## Usage of Non-Interactive version for scheduling with crontab

To run this, you need to run `python3 ni_run_cisco.py` or `python3 ni_run_huawei.py` in your terminal or command prompt. Host list will be taken from files `cisco_backup_hosts.csv` or `huawei_backup_hosts.csv`. So, please populate the right file depending on the vendor you are using.
It will copy the saved configuration into a folder named `backup-config` in the same directory of the python file. The configuration file name will be the Cisco device hostname, date, and time. Unreachable hosts will be listed in a separated file named `downDevices_` + date and time.

## Usage of Interactive version (Cisco Only)

To run this, you need to run `python3 i_run.py` in your terminal or command prompt. You'll get a prompt asking if you want to load the login information from a CSV file
or manually fill it in. If you choose the CSV option, you will need said CSV file in the same directory as the Python script.
It will copy the saved configuration into a folder named `backup-config` in the same directory of the python file. The configuration file name will be the Cisco device hostname, date, and time.
If you are on Linux or MacOS, you need to use `sudo python3 i_run.py` to run this due to the ping requiring permissions.

## Usage of multivendor Interactive version

Work in progress...

## How to test the software

This code was last tested March 9th, 2021. The dependencies you need to run it are Python3, PIP, Netmiko, and Ping3.

## Getting help

If you are having trouble or need help, create an issue [here](https://github.com/alexmunoz905/Python-Cisco-Backup/issues)

## Contributors
[ste-giraldo](https://github.com/ste-giraldo) for adding a memory and cpu saving feature to grabbing the hostname, and suggesting the ping feature.

## Credits and references

I'd like to credit Kirk Byers for making [Netmiko](https://github.com/ktbyers/netmiko), and Kyan for making [Ping3](https://github.com/kyan001/ping3)

----

## Licensing info

This code is with the MIT license.
