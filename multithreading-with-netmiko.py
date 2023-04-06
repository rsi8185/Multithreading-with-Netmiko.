import getpass
import sys
import time
import netmiko
import logging
import csv
import datetime
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

def configure_device(ip):
    try:
        connection_params = {
            "ip": ip.strip(),
            "device_type": "cisco_ios",
            "username": "test",
            "password": "test"
        }
        connection = netmiko.ConnectHandler(**connection_params)
    except:
        try:
            print(f"able to connect with Tacacs Cred--> {ip}")
            connection_params = {
                "ip": ip.strip(),
                "device_type": "cisco_ios",
                "username": "raj",
                "password": "raj"
            }
            connection = netmiko.ConnectHandler(**connection_params)
        except:
            print('Cannot connect to device {}, device may be down or not using standard credentials, logging to error log file'.format(ip))
            now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            with open("Devices_error.log", "a") as logf:
                logf.write(now)
                logf.write(" - Cannot connect to ")
                logf.write(ip + "\n")
            return

    try:
        with open('config.txt', 'r') as configfile:
            configset = configfile.read().splitlines()


        for line in configset:
            connection.send_config_set(line)
            time.sleep(2)


    except IOError:
        print('Error reading config.txt file')
        connection.disconnect()
        sys.exit(1)

    connection.disconnect()

if __name__ == "__main__":
    nodenum = 1

    try:
        with open('ExportDevice.CSV', 'r') as f:
            c = f.readlines()
    except IOError:
        print('Error reading ExportDevice.CSV file')
        sys.exit(1)

    max_threads = 2
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i in c:
            print("Device", nodenum, "- Checking IP Address", i)
            executor.submit(configure_device, i.strip())
            nodenum += 1

    print('Script has been pushed')
