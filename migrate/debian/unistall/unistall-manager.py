


#uniMgr = UniStallManager()
#uniMgr.find("Mozilla Firefox 75.0 (x64 de)")
from difflib import SequenceMatcher

def collectPkgsOfFindCmd(findCommand, findName):
    foundPkgNames = []

    #print("Executing: \"" + findCommand + "\" and looking for: " + findName)
    output = subprocess.run(findCommand.split(" "), capture_output=True, encoding="utf-8")
    #print(output.stderr)
    #print(output.stdout)
    outputLines = output.stdout.split("\n")
    #print(outputLines)

    for line in outputLines:
        #print("extracting from line: " + line)
        if(findName in line and "Name" not in line):
            #lineParts = line.split("\t")
            #print(lineParts)
            if(" " in line):
                nameEndStart = line.index(" ")
                #print(nameEndStart)
                name = line[0:int(nameEndStart)]
                foundPkgNames.append(name)

    return foundPkgNames

import re

#Regex to remove invalid characters for searching
blacklistRegex = re.compile("\(|\)")
minPartLength = 4
maximumPercentOfNumbers = 0.6
maxConsiderTerms = 4

def sanitize(term):
    return blacklistRegex.sub("",term)

def createSearchHierarchy(fullterm):
    hierarchyLevels = []

    toplevelname = fullterm.strip(" ").lower()
    toplevelname = toplevelname.replace(" ","")
    toplevelname = sanitize(toplevelname)
    if(len(toplevelname) >= minPartLength):
        #print("Appending toplevel: " + toplevelname)
        hierarchyLevels.append([toplevelname])
    else:
        hierarchyLevels.append([])

    nameParts = fullterm.split(" ")
    subTermParts = []
    
    for i in range(0,len(nameParts)):

        if(i >= maxConsiderTerms):
            break

        part = nameParts[i]

        sanitizedPart = sanitize(part)

        numbersCnt = sum(c.isdigit() for c in sanitizedPart)
        numbersPercent = numbersCnt/len(sanitizedPart)

        if(len(sanitizedPart) >= minPartLength and numbersPercent < maximumPercentOfNumbers):
            subTermParts.append(sanitizedPart.lower())

    #nameParts = map(lambda part: part.lower(), nameParts)
    hierarchyLevels.append(subTermParts)

    return hierarchyLevels

def createPkgScoreBoard(searchHierarchy,pkgManager):
    scoreBoardDict = {}
    #scoreBoardList = []

    for i in range(0,len(searchHierarchy)):
        searchLevel = searchHierarchy[i]

        for x in range(0,len(searchLevel)):
            searchTerm = searchLevel[x]

            levelTermPackages = pkgManager.find(searchTerm)
            for pkgName in levelTermPackages:
            
                if(pkgName not in scoreBoardDict):
                    # parts -> less exact matched -> lower base score
                    scoreBoardDict[pkgName] = 1.0/(i+1)
                    #scoreBoardList.append(pkgName)

                scoreBoardDict[pkgName] += SequenceMatcher(None, pkgName, searchTerm).ratio() * 1.0/(i+1)

                #Emphasise term postion (earlier terms are more important)
                scoreBoardDict[pkgName] *= 1.0 + (len(searchLevel) - x)/len(searchLevel)

    sortedDict = sorted(scoreBoardDict)
    return sortedDict

import subprocess

class SnapManager:

    def __init__(self):
        self.name = "snap"

    def find(self, packageTerm):
        command = "snap find " + packageTerm
        return collectPkgsOfFindCmd(command, packageTerm)

class FlatPakManager:
    #sudo apt install flatpak
    #flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    def __init__(self):
        self.name = "flatpak"

    def find(self, packageTerm):
        command = "flatpak search " + packageTerm
        return collectPkgsOfFindCmd(command, packageTerm)

class AptManager:

    def __init__(self):
        self.name = "apt"

    def find(self, packageTerm):
        command = "apt list"
        pkgs = collectPkgsOfFindCmd(command, packageTerm)
        pkgNameList = []
        for pkg in pkgs:
            parts = pkg.split("/")
            pkgNameList.append(parts[0])

        return pkgNameList

class UniStallManager:

    def __init__(self):
        self.packageManagers = []
        self.packageManagers.append(AptManager())
        self.packageManagers.append(SnapManager())
        self.packageManagers.append(FlatPakManager())

    def find(self, fuzzyTerm):
        print("Trying to find package for: " + fuzzyTerm)

        searchTermHierarchy = createSearchHierarchy(fuzzyTerm)
        
        for pkgManager in self.packageManagers:

            sortedPackages = createPkgScoreBoard(searchTermHierarchy, pkgManager)

            #nameResults = pkgManager.find(fuzzyTerm)
            print("Packages found with " + pkgManager.name)
            print(sortedPackages)
        

    def install(self, pkgName, pkgManager):
        print("Installing " + pkgName + " with " + pkgManager)

    def remove(self, pkgName):
        print("Trying to uninstall package: " + pkgName)


"""pkgManager = SnapManager()
results = pkgManager.find("firefox")
print(results)

pkgManager = AptManager()
results = pkgManager.find("firefox")
print(results)"""

pkgManager = UniStallManager()
results = pkgManager.find("Mozilla Firefox 75.0 (x64 de)")
#print(results)


"""import apt
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
"""