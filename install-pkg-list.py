import argparse
import os

parser = argparse.ArgumentParser(description='Execute install command with text file package lines')
parser.add_argument('filepath', help='Path to file containing package lines')

args = parser.parse_args()

filepath = args.filepath

with open(filepath) as file:
    firstline = file.readline()
    secondline = file.readline()

print()

if(not "\"\"\"" in secondline):

    command = firstline.replace("#","")
    command = command.replace("\n","")


    lineCommand = "python3 exec-cmd-txt-lines.py '" + command + "' " + filepath
    print("Executing: " + lineCommand)
    os.system(lineCommand)

else:
    print("File " + filepath + " commented out with \"\"\" skipping. \n")