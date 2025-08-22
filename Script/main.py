import paramiko
import plistlib
import io
from getpass import getpass
from art import tprint
from tabulate import tabulate


tprint("BAT UserDefaults Dumper")
print("by @Basel AbuTaleb\n\n")


host = input("[+] Enter device IP or hostname: ")
port = int(input("[+] Enter SSH port (default 22): ") or 22)
username = input("[+] Enter SSH username: ")
password = getpass("[+] Enter SSH password: ")

uuid = input("[+] Enter the app sandbox UUID: ")
bundle_id = input("[+] Enter the app bundle ID (e.g., com.example.myapp): ")

plist_path = f"/var/mobile/Containers/Data/Application/{uuid}/Library/Preferences/{bundle_id}.plist"

try:

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)


    sftp = ssh.open_sftp()
    with sftp.file(plist_path, 'rb') as f:
        plist_data = f.read()
        plist = plistlib.load(io.BytesIO(plist_data))

    sftp.close()
    ssh.close()


    table_data = [[idx+1, key, value] for idx, (key, value) in enumerate(plist.items())]
    table_headers = ["#", "Key", "Value"]


    print("\n--- UserDefaults ---")
    print(tabulate(table_data, headers=table_headers, tablefmt="grid", stralign="left"))

except Exception as e:
    print(f"Error: {e}")
