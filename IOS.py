from netmiko import ConnectHandler
import getpass

backupFile = open("running-config.txt", "w+")

host = input("IP: ")
username = input("Username: ")
password = getpass.getpass("Password: ")
enableSecret = getpass.getpass("Enable Secret: ")

cisco_router = {
    'device_type': 'cisco_ios',
    'host': host,
    'username': username,
    'password': password,
    'secret': enableSecret,
}

net_connect  = ConnectHandler(**cisco_router)
net_connect.enable()

output = net_connect.send_command("show running-config")
backupFile.write(output)
#print(output)
print("Outputted to running-config.txt!")