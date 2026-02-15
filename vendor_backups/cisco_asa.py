import os
from netmiko import ConnectHandler
from datetime import datetime

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")


# Gives us the information we need to connect to Cisco devices.
def backup(host, username, password, enable_secret):
    cisco_asa = {
        'device_type': 'cisco_asa',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_asa)
    net_connect.enable()
    # any reason not to use netmiko built-in func to find a hostname? Try it, and if you like it - replace everywhere. YW
    hostname = net_connect.find_prompt().replace('#', '').replace('>', '')
    if not hostname:
        # Gets and splits the hostname for the output file name.
        hostname = net_connect.send_command("show conf | i hostname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Gets the running configuration.
    output = net_connect.send_command("show run")

    # Creates the file name, which is the hostname, and the date and time.
    fileName = f"{hostname}_{dt_string}"
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    write_backup(fileName, output)
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName
