import argparse
import os
import lineparser as lineparse

parser = argparse.ArgumentParser(description='Convert windows program names to debian apt packages')
parser.add_argument('filepath', help='Path to file containing the windows program names')

args = parser.parse_args()

filepath = args.filepath

print(filepath)

aliasDict = {}
aliasAlternativeLines = lineparse.getFilteredFileLines("alias-alternatives-apt.txt")
for line in aliasAlternativeLines:

    lineParts = line.split("=")
    key = lineParts[0].rstrip(" ")
    value = lineParts[1].strip(" ")

    aliasList = [line]
    if(line.includes(',')):
        aliasList = value.split(',')
    
    aliasDict[key] = aliasList


def nameFromWinLine(line):
    return line


def autoResolve(winName):
    name = winName.strip(" ").lower()

winPkgLines = lineparse.getFilteredFileLines(filepath)
if(winPkgLines != None and len(winPkgLines) > 0):
    for line in lines:
        name = nameFromWinLine(line)

        #if(name in aliasDict):

