import os
from datetime import datetime

def write_backup(fileName: str, output: str):
# Current time and formats it to the North American time of Month, Day, and Year.
    dt_string = datetime.now().strftime("%m-%d-%Y_%H-%M")
    retval = f'{fileName}_{dt_string}.txt'
    backupPath = os.path.join('backup-config', retval)
    with open(backupPath, "w+") as backupFile:
        count = backupFile.write(output)
        pass 
    print(f"Outputted {count} bytes to {backupPath}")
    return retval


