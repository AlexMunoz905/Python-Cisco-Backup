from datetime import datetime
from datetime import date
from netmiko import ConnectHandler
import getpass

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

host = input("IP: ")
username = input("Username: ")
password = getpass.getpass("Password: ")
enableSecret = getpass.getpass("Enable Secret: ")

cisco_ios = {
    'device_type': 'cisco_ios',
    'host': host,
    'username': username,
    'password': password,
    'secret': enableSecret,
}

net_connect  = ConnectHandler(**cisco_ios)
net_connect.enable()

output = net_connect.send_command("show running-config")
result = net_connect.send_command("show run | in hostname")
result = result.split()
hostname = result[1]

backupFile = open("Output-Configs/" + hostname + ".txt", "w+")
backupFile.write(output)

fileName = hostname + "_" + dt_string

print("Outputted to " + fileName + ".txt!")