# Python Cisco Backup

Backup your saved Cisco configuration from your device to a folder with the hostname, date, and time. You have the option of having it all imported from a CSV file, or manually giving it the IP, Username, Password, and Enable Secret of each host.
This is running on Python3 with Netmiko.
Version 2.0

Manual Option:
![Screenshot of manual option](https://i.imgur.com/7SyRGe6.png)
CSV Option:
![Screenshot of CSV option](https://i.imgur.com/NOuNLoB.png)


## Use case of this program

The use case is that you are needing a backup of the saved configuration on your Cisco device.

## Installation

1. You must have Python3 and PIP installed on the device you are running the program on.
2. You need to run `pip3 install netmiko` or `pip install netmiko` in a command prompt / terminal on your computer.
3. You need to download this repository or copy all of the contents of the run.py file into a python file.

## Usage

To run this, you need to run `python3 run.py` in your terminal or command prompt. You'll get a prompt asking if you want to load the login information from a CSV file
or manually fill it in.
It will copy the saved configuration into a folder named `Output-Configs` in the same directory of the python file. The configuration file name will be the Cisco device hostname, date, and time.

## How to test the software

This code was last tested November 9th, 2020. The dependencies you need to run it are Python3, PIP, and Netmiko.

## Getting help

If you are having trouble or need help, create an issue [here](https://github.com/alexmunoz905/Python-Cisco-Backup/issues)

## Credits and references

I'd like to credit Kirk Byers for making [Netmiko](https://github.com/ktbyers/netmiko)

----

## Licensing info

This code is with the MIT license.
