# Python Cisco Backup

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/AlexMunoz905/Python-Cisco-Backup)

Backup your saved Cisco configuration from your device to a folder with the hostname, date, and time. You have the option of having it all imported from a CSV file or manually giving it the IP, Username, Password, and Enable Secret of each host.

This program runs on Python3 with Netmiko and ping3.
Version 2.0

**Manual Option:**

![Screenshot of manual option](https://i.imgur.com/7SyRGe6.png)

**CSV Option:**

![Screenshot of CSV option](https://i.imgur.com/NOuNLoB.png)

## Use case of this program

The use case is that you need a backup of the saved configuration on your Cisco device.

## Installation

```bash
$ git clone https://github.com/AlexMunoz905/Python-Cisco-Backup.git
$ cd Python-Cisco-Backup
$ pip install -r requirements.txt
```

## Usage

```python3
python/python3 run.py
```

You will get a prompt asking if you want to load the login information from a CSV file or to manually fill it in. If you choose the CSV option, you will need to seed a CSV file in the same directory as the Python script. It will copy the saved configuration into a folder called `Output-Configs` in the same directory of the python file. The configuration file name will be the Cisco device hostname, date, and time. If you are using Linux or macOS, you will need to use `sudo python3 run.py` to run this due to the ping permissions. Windows requires no permissions on my testing.

## How to test the software

This code was last tested March 9th, 2021. The dependencies you need to run it are Python3, PIP, Netmiko, and Ping3.

## Getting help

If you are having trouble or need help, create an issue [here](https://github.com/alexmunoz905/Python-Cisco-Backup/issues)

## Contributors

[ste-giraldo](https://github.com/ste-giraldo) for adding a memory and CPU saving feature to grabbing the hostname and suggesting the ping feature.

## Credits and references

I'd like to credit Kirk Byers for making [Netmiko](https://github.com/ktbyers/netmiko), and Kyan for making [Ping3](https://github.com/kyan001/ping3)

---

## Licensing info

This code is licensed under the MIT license.
