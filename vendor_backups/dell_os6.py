from netmiko import ConnectHandler
from .lib import write_backup

# Gives us the information we need to connect to Cisco devices.
def backup(host, username, password, enable_secret):
    dell_os6 = {
        "device_type": "dell_os6",
        "host": host,
        "username": username,
        "password": password,
        "secret": enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**dell_os6)
    net_connect.enable()
    # any reason not to use netmiko built-in func to find a hostname? Try it, and if you like it - replace everywhere. YW
    hostname = net_connect.find_prompt().replace("#", "").replace(">", "")
    if not hostname:
        # Gets and splits the hostname for the output file name.
        hostname = net_connect.send_command("show conf | i hostname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Gets the running configuration.
    output = net_connect.send_command("terminal length 0")
    output = net_connect.send_command("show run")
    #
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    fileName = write_backup(hostname, output)
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName

