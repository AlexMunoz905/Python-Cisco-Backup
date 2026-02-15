import os

def write_backup(fileName: str, output: str):
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backup_file = os.path.join("backup-config", f"{fileName}.txt")
    with open(backup_file, "w") as backupFile:
        backupFile.write(output)
        pass

    print(f"Outputted to {len(output)} bytes to {backup_file}")

