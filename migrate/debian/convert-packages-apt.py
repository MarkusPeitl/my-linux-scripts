import argparse
import os
import lineparser as lineparse
import re
import subprocess
from difflib import SequenceMatcher


parser = argparse.ArgumentParser(description='Convert windows program names to debian apt packages')
parser.add_argument('filepath', help='Path to file containing the windows program names')

args = parser.parse_args()

filepath = args.filepath

print("Consuming software list: " + filepath + "\n")

blackListRegEx = re.compile("windows|microsoft|nvidia|intel|amd|update|visual c|winrt|arm|msi| pack |redist|localization|installer|package")

print("Making alias dictionary")
aliasDict = {}
aliasAlternativeLines = lineparse.getFilteredFileLines("alias-alternatives-apt.txt")
for line in aliasAlternativeLines:

    print(line)

    lineParts = line.split("=")
    key = lineParts[0].rstrip(" ")
    value = lineParts[1].strip(" ")

    aliasList = [line]
    if(',' in line):
        aliasList = value.split(',')
    
    aliasDict[key] = aliasList

print()

def nameFromWinLine(line):
    return line.split(',')[0].replace("\"","")

def extractCandidates(winName):

    if(blackListRegEx.search(winName.lower())):
        return None

    lowerWinName = winName.lower()

    candidates = []
    candidates.append(lowerWinName)
    candidates.append(lowerWinName.strip(" "))
    candidates.append(lowerWinName.split(" "))

    numbers = sum(c.isdigit() for c in lowerWinName)


    return candidates

    #name = winName.strip(" ").lower()
    #nameParts = winName.split(" ")

    #return " ".join(nameParts)
    #return nameParts[0].lower()

def softwareIsBlacklisted(softname):
    if(blackListRegEx.search(softname.lower())):
        return True
    return False

def matchSubstringList(subString,fullNamesList):
    foundPackages = None
    for pkgName in fullNamesList:
        if (subString in pkgName):

            if(foundPackages is None):
                foundPackages = []

            foundPackages.append(pkgName)
            #print(pkg)

    return foundPackages

def promptPickFromList(pkgNamesList):
    for i in range(0,len(pkgNamesList)):
        print(str(i) + ") " + pkgNamesList[i])

    if response is not "n":
        if(response.isnumeric()):
            return foundPackages[int(response)]
    else:
        print("None selected skipping")
        return None

def lookFor(softwareTerms):
    #output = subprocess.run("apt list | grep firefox".split(" "), capture_output=True,shell=True)
    #output = subprocess.run("apt-get list --installed".split(" "), capture_output=True,shell=True)
    #output = subprocess.check_output("apt-get list | grep firefox".split(" "), universal_newlines=True)
    #print("After search")
    #print(output)
    softwareTerms = ["firefox","thunderbird"]

    """pkgManager = "apt"
    pkgNames = map(lambda pkg: pkg.name, apt.Cache())

    for softwareCandidate in softwareTerms:
        
        foundPackages = matchSubstringList(softwareTerms,pkgNames)
        selectedPackage = promptPickFromList(foundPackages)

        if(selectedPackage != None):
            return selectedPackage, pkgManager

    return None, None
    """

print("Extracting win software names")

def searchProgramMatches(term,hint):
    return term

import apt
class AptManager:

    def __init__(self):
        self.type = "apt"
        #cache = apt.cache.Cache()
        #cache.update()
        #cache.open()

    def createPkgScoreBoard(self,fullterm):
        scoreBoardDict = {}
        scoreBoardList = []

        levels = []
        #Top level is an exact match
        toplevelname = fullterm.strip(" ").lower()
        levels.append([toplevelname])
        nameParts = fullterm.split(" ")
        nameParts = map(lambda part: part.lower(), nameParts)
        levels.append(nameParts)

        topLvlPkgs = self.findPackages(toplevelname)
        if(topLvlPkgs is not None):
            for pkg in topLvlPkgs:
                
                if(pkg not in scoreBoardDict):
                    scoreBoardDict[pkg] = 1.0
                    scoreBoardList.append(pkg)

                scoreBoardDict[pkg] += SequenceMatcher(None, pkg, toplevelname).ratio()

        for partialName in nameParts:

            partialFoundPackages = self.findPackages(partialName)
            if(partialFoundPackages is not None):
                for pkg in partialFoundPackages:
                    
                    if(pkg not in scoreBoardDict):
                        scoreBoardDict[pkg] = 0.5
                        scoreBoardList.append(pkg)
                    
                    scoreBoardDict[pkg] += SequenceMatcher(None, pkg, partialName).ratio() * 0.5


        sortedDict = sorted(scoreBoardDict)
        return sortedDict


    def findPackages(self,pkgNamePart):
        pkgNames = map(lambda pkg: pkg.name, apt.Cache())

        foundPackages = matchSubstringList(pkgNamePart,pkgNames)
        return foundPackages


    def lookFor(self,pkgNamePart):
        #pkgManager = "apt"
        pkgNames = map(lambda pkg: pkg.name, apt.Cache())

        foundPackages = matchSubstringList(pkgNamePart,pkgNames)
        selectedPackage = promptPickFromList(foundPackages)

        if(selectedPackage != None):
            return selectedPackage

        return None

    def install(self,pkgName):

        pkg = cache[pkgName]

        if pkg.is_installed:
            print("apt package already installed - exitting -> " + pkgName)
            return 1
        else:
            pkg.mark_install()

            try:
                cache.commit()
                return 0

            except Exception as arg:
                print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))

            return -1

class SnapManager:

    def __init__(self):
        self.type = "snap"
        #cache = apt.cache.Cache()
        #cache.update()
        #cache.open()

    def lookFor(self,pkgNamePart):
        search = "snap find " + pkgNamePart

        """pkgNames = map(lambda pkg: pkg.name, apt.Cache())

        foundPackages = matchSubstringList(pkgNamePart,pkgNames)
        selectedPackage = promptPickFromList(foundPackages)

        if(selectedPackage != None):
            return selectedPackage, pkgManager"""

        return None


    def install(self,pkgName):
        cmd = "sudo snap install " + pkgName
        print("Installing snap -> " + cmd)

packageManagerMgrs = []


aptmgr = AptManager()
winPkgLines = lineparse.getFilteredFileLines(filepath)
if(winPkgLines != None and len(winPkgLines) > 0):
    for line in winPkgLines:

        name = nameFromWinLine(line)
        #resolved = extractCandidates(name)
        if(not softwareIsBlacklisted(name)):

            response = input("look for package in: \"" + name + "\" ? (y/ )")
            if(response.strip(" ") is "y"):
                print()
                print("Looking for package: \"" + name + "\" ............................")

                sortedPkgs = aptmgr.createPkgScoreBoard(name)
                print(sortedPkgs)

                """foundPackage, pkgmanager = lookFor(name)
                if(foundPackage is not None and pkgManager is not None):
                    print("Found package: " + foundPackage " in " + pkgManager)
                else
                    print("Failed to find software package")
                """

                #print("\n".join(resolved))
                #print(resolved)
                print()

            
        #print(name)
        #if(name in aliasDict):


#Hierarical Find
# 1st layer "Native Instruments Kontakt" = "nativeinstrumentskontakt"
# 2nd layer "nativeinstruments" "nativekontakt" "instrumentskontakt"
# 3rd layer "native" "instruments" "kontakt"

#Execute 1st layer for each package Manager -> list curated results
# ask if install package | continue searching in deeper layer | give up finding package

# "Python 3.7.7 Executables (64-bit)" = "python3.7.7executables(64-bit)"
# "python3.7.7executables" , "3.7.7executables(64-bit)"
# "python3.7.7" , "3.7.7executables", "executables(64-bit)" , "python(64-bit)", "pythonexecutables", "3.7.7(64-bit)"
# "python", "3.7.7", "executables", "(64-bit)"


#Not enough results in 1 layer -> auto search the next ones

# Earlier word in the title more important ( for search (not exact match))
# Only use first 3-5 words for search


# Grep Union + order ?? (bottom up) -> match single words and grade multi matches higher



#also try Join name by "-" instead of ""




# Always show the most likely candidates 0-9 (a = show all | (n/ ) = exit | d = down hierarchy )