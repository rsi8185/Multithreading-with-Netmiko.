# Multithreading-with-Netmiko

The purpose of this code is to automate the configuration of multiple Cisco IOS devices using the Netmiko library in Python. I
it reads a list of IP addresses from a CSV file, connects to each device using either a default or alternate set of credentials, 
reads a configuration file, and applies the configuration to each device in the list. The code also includes error handling and 
logging functionality to track failed connection attempts and configuration errors. It utilizes multiprocessing to speed up the 
configuration process by processing multiple devices concurrently.

Here is a line-by-line explanation of the code:
**************************************************************************************************************************************************************
	
	import getpass
	import sys
	import time
	import netmiko
	import logging
	import csv
	import datetime
	from concurrent.futures import ThreadPoolExecutor

These are Python modules being imported. getpass module is used to handle password input, sys module provides access to some variables used or maintained by the interpreter, time module provides various time-related functions, netmiko module is used to handle network devices, logging module provides a flexible event logging system for applications, csv module implements classes to read and write tabular data in CSV format, datetime module supplies classes for working with dates and times, and ThreadPoolExecutor class from concurrent.futures module is used for parallel execution of the configuration commands on multiple devices.

**************************************************************************************************************************************************************
Debug logs

	logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
	logger = logging.getLogger("netmiko")

These lines configure the logging module to log debug messages to the specified file, 'netmiko_global.log'.

**************************************************************************************************************************************************************
Funtion
	
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

This function 'configure_device' takes an IP address as input and tries to connect to the device using Netmiko's ConnectHandler() function with provided login credentials. If it fails to connect, it retries with different credentials. If it still fails to connect, it logs an error message to the 'Devices_error.log' file.

****************************************************************************************************************************************************************


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

These lines try to open the 'config.txt' file which contains a list of configuration commands to be executed on the device. If it is successful, it sends each command to the device using the 'send_config_set' function of the connection object. It also sleeps for 2 seconds after each command to avoid overloading the device with commands. If it fails to open the file, it disconnects from the device and terminates the script with an error message.

****************************************************************************************************************************************************************

	

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
    
   This code block is a Python idiom that checks if the script is being run as the main program. The __name__ variable is a special variable in Python that is set to "__main__" when the script is run as the main program, but is set to the name of the module when the script is imported as a module into another program.

Inside the if __name__ == "__main__": block, the code does the following:

Sets the initial value of nodenum to 1
Attempts to open a file named ExportDevice.CSV in read mode and reads all the lines into a list c
Creates a thread pool executor object with a maximum number of threads set to 2.
For each IP address in the c list, it prints a message indicating the device number and the IP address being checked, and submits a new thread to execute the configure_device function with the IP address as an argument.
After submitting all the threads, it prints a message indicating that the script has been pushed.
In summary, this code reads a list of IP addresses from a CSV file and executes the configure_device function in parallel for each IP address using a thread pool with a maximum of 2 threads.

****************************************************************************************************************************************************************


