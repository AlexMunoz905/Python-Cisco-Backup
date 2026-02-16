from netmiko import ConnectHandler
from .lib import write_backup

# Gives us the information we need to connect to MicroTik devices.
def backup(host, username, password):
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
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = net_connect.send_command("system identity print")
        hostname = hostname.split()
        hostname = hostname[1]
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    fileName = write_backup(hostname, output)
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName
