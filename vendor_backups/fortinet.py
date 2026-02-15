from netmiko import ConnectHandler
from datetime import datetime

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect to Fortinet devices.
def backup(host, username, password):
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
    hostname = net_connect.find_prompt().replace('#','').replace('>','')
    if not hostname:
        hostname = host
        fileName = host + "_" + dt_string
    else:
        fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    write_backup(fileName, output)
    # For the GUI
    global gui_filename_output
    gui_filename_output = fileName
