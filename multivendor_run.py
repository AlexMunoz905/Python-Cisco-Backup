# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader
from datetime import datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
from vendor_backups import cisco,fortinet,huawei,juniper,microtik,vyos
import getpass
import os
import sys
import time
import cmd

# Speciefied CSV file for the script to grab the hosts from.
csv_name = "dev_hosts.csv"

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gets the CSV file name for Cisco devices, and grabs the information from it.
def csv_option_cisco():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_Cisco_Devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                cisco.get_saved_config_cisco(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Gets the CSV file name for Juniper devices, and grabs the information from it.
def csv_option_juniper():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_Juniper_Devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                juniper.get_saved_config_juniper(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for Fortinet devices, and grabs the information from it.
def csv_option_fortinet():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_Fortinet_Devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                fortinet.get_saved_config_fortinet(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for VyOS devices, and grabs the information from it.
def csv_option_vyos():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_VyOS_Devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                vyos.get_saved_config_vyos(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for Huawei devices, and grabs the information from it.
def csv_option_huawei():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_Huawei_boxes_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                huawei.get_saved_config_huawei(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for MicroTik devices, and grabs the information from it.
def csv_option_microtik():
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_microtik_devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                microtik.get_saved_config_microtik(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Asks the user what option they are going to use.
print("\n1. Backup Cisco IOS devices.")
print("2. Backup Juniper devices.")
print("3. Backup VyOS routers.")
print("4. Backup Huawei boxes.")
print("5. Backup Fortinet devices.")
print("6. Backup MicroTik devices.\n")
choice = input("Please pick an option: ")

# This basically runs the whole file.
if choice == "1":
  csv_option_cisco()
elif choice == "2":
  csv_option_juniper()
elif choice == "3":
  csv_option_vyos()
elif choice == "4":
  csv_option_huawei()
elif choice == "5":
    csv_option_fortinet()
elif choice == "6":
    csv_option_microtik()
