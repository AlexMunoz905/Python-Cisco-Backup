from csv import reader
from datetime import datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
from vendor_backups import cisco,fortinet,huawei,juniper,microtik,vyos
import os
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter import messagebox

# Initializes Tkinter
root = Tk()
root.title("Backup Configurator")
tk_frame = Frame(root)
tk_frame.pack(expand=True)

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Popup window that tells that the backup worked
def backup_completion_popup(backup_file_name):
    messagebox.showinfo("Configuration Backup","Saved To: " + backup_file_name)

# Popup window that tells user each down host
def down_host_popup(down_host_ip):
    messagebox.showinfo("Down Host","Down Host: " + down_host_ip)

# Main function.
def run_script(user_selection):
    file_path = askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as read_obj:
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
                    down_host_popup(str(ip))
                else:
                    # Based on user selection, run the script in the vendor_backups folder. The passed variables are hosts, username, password, and optional secret.
                    if user_selection == "1":
                        cisco.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
                        backup_completion_popup(cisco.gui_filename_output)
                    elif user_selection == "2":
                        juniper.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                        backup_completion_popup(juniper.gui_filename_output)
                    elif user_selection == "3":
                        vyos.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                        backup_completion_popup(vyos.gui_filename_output)
                    elif user_selection == "4":
                        huawei.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                        backup_completion_popup(huawei.gui_filename_output)
                    elif user_selection == "5":
                        fortinet.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                        backup_completion_popup(fortinet.gui_filename_output)
                    elif user_selection == "6":
                        microtik.backup(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2])
                        backup_completion_popup(microtik.gui_filename_output)

# Build the button and assign values
tk_cisco = Button(tk_frame, text="Cisco", command=lambda : run_script("1"))
tk_juniper = Button(tk_frame, text="Juniper", command=lambda : run_script("2"))
tk_vyos = Button(tk_frame, text="VyOS", command=lambda : run_script("3"))
tk_huawei = Button(tk_frame, text="Huawei", command=lambda : run_script("4"))
tk_fortinet = Button(tk_frame, text="Fortinet", command=lambda : run_script("5"))
tk_microtik = Button(tk_frame, text="Microtik", command=lambda : run_script("6"))

# Place the button on the GUI
tk_cisco.pack(side=LEFT, padx=5, fill=BOTH, expand=True)
tk_juniper.pack(side=LEFT, padx=5, fill=BOTH, expand=True)
tk_vyos.pack(side=LEFT, padx=5, fill=BOTH, expand=True)
tk_huawei.pack(side=LEFT, padx=5, fill=BOTH, expand=True)
tk_fortinet.pack(side=LEFT, padx=5, fill=BOTH, expand=True)
tk_microtik.pack(side=LEFT, padx=5, fill=BOTH, expand=True)

# Runs the gui
mainloop()