#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():  # Function to get user input
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface_name", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) =parser.parse_args()
    if not options.interface_name:
        parser.error("[-] Please specify an interface name, use --help for more info.")  # Error check for Interface
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")  # Error check for MAC
    return options


def change_mac(interface_name, new_mac):  # Function to change mac address
    subprocess.call(["ifconfig", interface_name, "down"])
    subprocess.call(["ifconfig", interface_name, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface_name, "up"])


def get_current_mac(interface):  # Function to get current mac address
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)) # Ifconfig result is machine readable while regex is human readable
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface_name)
print("current mac = "+str(current_mac))

change_mac(options.interface_name, options.new_mac)

current_mac = get_current_mac(options.interface_name)
if current_mac == options.new_mac:
    print("[+] MAC address was changed successfully to " + current_mac)
else:
    print("[-] MAC address did not change.")

