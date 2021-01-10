import argparse
#import subprocess
#from subprocess import Popen, PIPE, STDOUT
import os

parser = argparse.ArgumentParser(description='Execute install command with text file package lines')
parser.add_argument('command', help='command to execute passing the packages')
parser.add_argument('filepath', help='Path to file containing package lines')

args = parser.parse_args()

command = args.command
filepath = args.filepath

print("\n")

print("Executing command " + command + " with args from " + filepath)

print()

file = open(filepath, "r")
for line in file:
    if(len(line) > 1 and line[0] != "#"):

        package = line.replace("\n","")
        #package = package.replace(" ","")

        lineCommand = command + " " + package
        print("     Executing: " + lineCommand)
        os.system(lineCommand)
        print()
        #subprocess.run(lineCommand.split(" "), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
