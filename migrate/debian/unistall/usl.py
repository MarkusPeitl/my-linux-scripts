import argparse
import os
from import UniStallManager

parser = argparse.ArgumentParser(description='UNI stall manager')
parser.add_argument('-f','--find', help='Find a package in the pkgmanager repositories')
parser.add_argument('-fi','--findinstall', help='Find a package in the pkgmanager repositories and install')
parser.add_argument('-i','--install', help='Path to file containing the windows program names')

args = parser.parse_args()

findinstall = args.findinstall.replace("\"","")

uslManager = UniStallManager()

if(findinstall != None):
    uslManager.findinstall(findinstall)

#print(filepath)