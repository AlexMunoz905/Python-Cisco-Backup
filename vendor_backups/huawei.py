from netmiko import ConnectHandler
from .lib import write_backup

# Gives us the information we need to connect to Huawei devices.
def backup(host, username, password):
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
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = net_connect.send_command("dis saved-configuration | inc sysname")
        hostname = hostname.split()
        hostname = hostname[1]
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    fileName = write_backup(hostname, output)
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName
