# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader
from datetime import datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
from vendor_backups import cisco,fortinet,huawei,juniper,microtik,vyos
import os

# Speciefied CSV file for the script to grab the hosts from.
csv_name = "backup_hosts.csv"

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

def run_script(user_selection):
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                if user_selection == "1":
                    cisco.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
                elif user_selection == "2":
                    juniper.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "3":
                    vyos.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "4":
                    huawei.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "5":
                    fortinet.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "6":
                    microtik.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])

# Asks the user what option they are going to use.
print("\n1. Backup Cisco IOS devices.")
print("2. Backup Juniper devices.")
print("3. Backup VyOS routers.")
print("4. Backup Huawei boxes.")
print("5. Backup Fortinet devices.")
print("6. Backup MicroTik devices.\n")

user_selection = input("Please pick an option: ")

run_script(user_selection)