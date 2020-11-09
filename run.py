# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
import getpass
import os

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('Output-Configs'):
    os.makedirs('Output-Configs')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect.
def get_saved_config(host, username, password, enable_secret):
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
    # Gets the running configuration.
    output = net_connect.send_command("show running-config")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show run | in hostname")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the Output-Configs folder with the special name, and writes to it.
    backupFile = open("Output-Configs/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt!")

# Asks for the IP, Username, Password, and Enable Secret, and passes it along to the get_saved_config function.
def manual_option():
    host = input("\nIP: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    enable_secret = getpass.getpass("Enable Secret: ")
    get_saved_config(host, username, password, enable_secret)

# Gets the CSV file name, and grabs the information from it.
def csv_option():
    csv_name = input("\nWhat is the name of your CSV file?: ")
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])

# Asks the user what option they are going to use.
print("\n1. Input information your self.")
print("2. Input information directly from CSV file.\n")
choice = input("Please pick an option: ")

# This basically runs the whole file.
if choice == "1":
    # Figures out how many hosts the user is going to manually input.
    how_many = input("How many hosts?: ")
    how_many = int(how_many)
    i = how_many
    while i >= 1:
        manual_option()
        i = i - 1
elif choice == "2":
    # Runs the whole CSV option.
    csv_option()
