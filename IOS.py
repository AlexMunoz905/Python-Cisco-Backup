from netmiko import ConnectHandler
import getpass

host = input("IP: ")
username = input("Username: ")
password = getpass.getpass("Password: ")
enableSecret = getpass.getpass("Enable Secret: ")

backupFile = open("Output-Configs/" + host + ".txt", "w+")

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
backupFile.write(output)
#print(output)
print("Outputted to running-config.txt!")