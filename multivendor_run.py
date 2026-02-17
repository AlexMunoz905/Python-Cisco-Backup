# All pre-installed besides Netmiko and ping3.
import os
from csv import reader
from datetime import datetime
# 3rd party
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
# package libraries
from vendor_backups import cisco_ios,cisco_asa,fortinet,huawei,juniper,microtik,vyos,dell_os6

# Specified CSV file for the script to grab the hosts from.
csv_name = "backup_hosts.csv"

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Main function.
def run_script(user_selection):
    # Imports the CSV file specified in the csv_name variable.
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            # Pings the hosts in the CSV file, successful pings move onto the else statement.
            # Unsuccessful pings go into a down_devices file.
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "down_devices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                # Based on user selection, run the script in the vendor_backups folder. The passed variables are hosts, username, password, and optional secret.
                if user_selection == "1":
                    cisco_ios.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
                elif user_selection == "2":
                    cisco_asa.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
                elif user_selection == "3":
                    juniper.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "4":
                    vyos.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "5":
                    huawei.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "6":
                    fortinet.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "7":
                    microtik.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                elif user_selection == "8":
                    dell_os6.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Asks the user what option they are going to use.
print("\n1. Backup Cisco IOS devices.")
print("2. Backup Cisco ASA devices.")
print("3. Backup Juniper devices.")
print("4. Backup VyOS routers.")
print("5. Backup Huawei boxes.")
print("6. Backup Fortinet devices.")
print("7. Backup MicroTik devices.")
print("8. Backup Dell OS6 devices.\n")
user_selection = input("Please pick an option: ")
# Pass the users choice to the main function.
run_script(user_selection)
