# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
import getpass
import os
import sys
import time
import cmd

#sys.tracebacklimit = 0

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect to Cisco devices.
def get_saved_config_cisco(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    #any reason not to use netmiko built-in func to find a hostname? Try it, and if you like it - replace everywhere. YW
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        # Gets and splits the hostname for the output file name.
        hostname = net_connect.send_command("show conf | i hostname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gives us the information we need to connect to Juniper devices.
def get_saved_config_juniper(host, username, password,):
    juniper = {
        'device_type': 'juniper',
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**juniper)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show conf | display set")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | match hostname")
    hostname = hostname.split()
    hostname = hostname[2]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gives us the information we need to connect to Fortinet devices.
def get_saved_config_fortinet(host, username, password,):
    fortinet = {
        'device_type': 'fortinet',
        'host': host,
        'username': username,
        'password': password
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**fortinet)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show")

    # Creates the file name, which is the hostname, and the date and time.
    fileName = host + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt!")

# Gives us the information we need to connect to VyOS devices.
def get_saved_config_vyos(host, username, password,):
    vyos = {
        'device_type': 'vyos',
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**vyos)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show conf comm")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("sh conf | grep host-name | awk {'print $2'}")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gives us the information we need to connect to Huawei devices.
def get_saved_config_huawei(host, username, password,):
    huawei = {
        "device_type": "huawei",
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler (** huawei)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("dis current-configuration")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("dis saved-configuration | inc sysname")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gives us the information we need to connect to MicroTik devices.
def get_saved_config_microtik(host, username, password,):
    microtik = {
        'device_type': 'mikrotik_routeros',
        'host': host,
        'username': username,
        'password': password,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**microtik)
    # Gets the running configuration.
    output = net_connect.send_command_timing("export", delay_factor=40)
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("system identity print")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = "config_backup-" + hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")

# Gets the CSV file name for Cisco devices, and grabs the information from it.
def csv_option_cisco():
    csv_name = input("\nWhat is the name of your CSV file for Cisco devices?: ")
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
                get_saved_config_cisco(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Gets the CSV file name for Juniper devices, and grabs the information from it.
def csv_option_juniper():
    csv_name = input("\nWhat is the name of your CSV file for Juniper devices?: ")
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
                get_saved_config_juniper(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for Fortinet devices, and grabs the information from it.
def csv_option_fortinet():
    csv_name = input("\nWhat is the name of your CSV file for Fortinet devices?: ")
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
                get_saved_config_fortinet(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for VyOS devices, and grabs the information from it.
def csv_option_vyos():
    csv_name = input("\nWhat is the name of your CSV file for VyOS routers?: ")
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
                get_saved_config_vyos(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for Huawei devices, and grabs the information from it.
def csv_option_huawei():
    csv_name = input("\nWhat is the name of your CSV file for Huawei boxes?: ")
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
                get_saved_config_huawei(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Gets the CSV file name for MicroTik devices, and grabs the information from it.
def csv_option_microtik():
    csv_name = input("\nWhat is the name of your CSV file for MicroTik boxes?: ")
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
                get_saved_config_huawei(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

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
