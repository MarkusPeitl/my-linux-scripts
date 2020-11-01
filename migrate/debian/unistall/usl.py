#!/usr/bin/python3

# Possible names: universeinstaller (uvi), unistaller (usl), unistallmanager (umgr)

import argparse
import os
import unistallmanager

parser = argparse.ArgumentParser(description='UNI stall manager')

parser.add_argument('-f','--find', help='Find a package in the pkgmanager repositories')
parser.add_argument('-i','--install', help='Find a package in the pkgmanager repositories and install')
parser.add_argument('-r','--remove', help='Remove and intstalled package')
parser.add_argument('-o','--open', help='Find and open a program on the system')

args = parser.parse_args()

installPackage = args.install.replace("\"","")

uslManager = unistallmanager.UniStallManager()

if(installPackage != None):
    uslManager.findinstall(installPackage)

#print(filepath)

#make me executable "chmod +x usl.py"
# executable by ./usl.py

# export PATH=$PATH:~/repos/my-linux-scripts/migrate/debian/unistall
# Add to end "nano ~/.bashrc"