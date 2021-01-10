


#uniMgr = UniStallManager()
#uniMgr.find("Mozilla Firefox 75.0 (x64 de)")
from difflib import SequenceMatcher
import os

def collectLinesOfCommand(findCommand):
    foundPkgNames = []

    #print("Executing: \"" + findCommand + "\" and looking for: " + findName)
    output = subprocess.run(findCommand.split(" "), capture_output=True, encoding="utf-8")
    #print(output.stderr)
    #print(output.stdout)
    return output.stdout.split("\n")
    #print(outputLines)

    """for line in outputLines:
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
    """

import re

#Regex to remove invalid characters for searching
blacklistRegex = re.compile("\(|\)|\+")
minTopLength = 3
minPartLength = 4
maximumPercentOfNumbers = 0.6
maxConsiderTerms = 4
replaceWhitespaceRegex = re.compile("[ ]+")

def sanitize(term):
    return blacklistRegex.sub("",term)

def createSearchHierarchy(fullterm):
    hierarchyLevels = []

    toplevelname = fullterm.strip(" ").lower()
    toplevelname = toplevelname.replace(" ","")
    toplevelname = sanitize(toplevelname)
    if(len(toplevelname) >= minTopLength):
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
            for pkgInfo in levelTermPackages:
                pkgName = pkgInfo["name"]

                if(pkgName not in scoreBoardDict):
                    # parts -> less exact matched -> lower base score
                    scoreBoardDict[pkgName] = pkgInfo
                    
                    scoreBoardDict[pkgName]["score"] = 1.0/(i+1)
                    #scoreBoardList.append(pkgName)
                scorePkgEntry = scoreBoardDict[pkgName]

                #Emphasise term postion (earlier terms are more important)
                scorePkgEntry["score"] *= 1.0 + (len(searchLevel) - x)/len(searchLevel)

                exactNess = SequenceMatcher(None, pkgName, searchTerm).ratio()
                #scoreBoardDict[pkgName] += (SequenceMatcher(None, pkgName, searchTerm).ratio() - 0.5) * 1.0/(i+1)
                scorePkgEntry["score"] += scorePkgEntry["score"] * exactNess
                

    #sortedDict = sorted(scoreBoardDict)
    return scoreBoardDict

import subprocess

class SnapManager:

    def __init__(self):
        self.name = "snap"

    def find(self, packageTerm):
        command = "snap find " + packageTerm
        pkgLines = collectLinesOfCommand(command)

        foundPkgInfos = []
        if(len(pkgLines) > 0):
            header = pkgLines[0]
            headerParts = replaceWhitespaceRegex.sub(" ", header).split(" ")

            for i in range(1,len(pkgLines)):
                if(packageTerm in pkgLines[i].lower()):
                    packageLine = pkgLines[i]
                    if(len(packageLine) > 8):
                        
                        #print("extracting from line: " + packageLine)
                        lineParts = replaceWhitespaceRegex.sub(" ", packageLine).split(" ")

                        pkgInfo = {
                            "name": lineParts[0],
                            "installid": lineParts[0],
                            "version": lineParts[1],
                            "publisher": lineParts[2],
                            "notes": lineParts[3],
                            "description": " ".join(lineParts[4:]),
                            "pkgmgr": self.name
                        }

                    foundPkgInfos.append(pkgInfo)

        return foundPkgInfos

    def install(self,packageDef):

        flags = ""

        if("notes" not in packageDef or "classic" in packageDef["notes"]):

            print("0) strict sandboxed - default")
            print("1) classic - app has access to system")
            print("e) exit app installation")
            response = input("Confinement mode? ")
            

            if(len(response) > 0):
                if(response.isnumeric() and int(response) >= 0 and int(response) <=1):
                    if(int(response) == 1):
                        flags = " --classic"
                elif response == "e":
                    return False
                else:
                    print("Invalid option")
                    return self.install(packageDef)
            

        command = "snap install " + packageDef["installid"] + flags
        print("Executing install: " + command)
        os.system(command)
        return True

class FlatPakManager:
    #sudo apt install flatpak
    #flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    def __init__(self):
        self.name = "flatpak"

    def find(self, packageTerm):
        command = "flatpak search " + packageTerm
        pkgLines = collectLinesOfCommand(command)
        #print(pkgLines)

        foundPkgInfos = []
        if(len(pkgLines) > 0):
            header = pkgLines[0]
            header = header.replace("Application ID","ApplicationID")
            headerParts = replaceWhitespaceRegex.sub(" ", header).split(" ")


            for i in range(0,len(pkgLines)):
                #print("extracting from line: " + pkgLines[i] + " -> term: " + packageTerm)
                if(packageTerm in pkgLines[i].lower()):
                    packageLine = pkgLines[i]
                    if(len(packageLine) > 8):
                        #print("extracting from line: " + packageLine)
                        #lineParts = replaceWhitespaceRegex.sub(" ", packageLine).split(" ")
                        lineParts = packageLine.split("\t")

                        pkgInfo = {
                            "name": lineParts[0],
                            "installid": lineParts[2],
                            "version": lineParts[3],
                            "description": lineParts[1],
                            "pkgmgr": self.name
                        }

                        foundPkgInfos.append(pkgInfo)

        return foundPkgInfos

    def install(self,packageDef):
        command = "flatpak install " + packageDef["installid"]
        print("Executing install: " + command)
        os.system(command)
        return True

class AptManager:

    def __init__(self):
        self.name = "apt"

    def find(self, packageTerm):
        command = "apt list"
        pkgLines = collectLinesOfCommand(command)

        foundPkgInfos = []
        if(len(pkgLines) > 0):
            for i in range(1,len(pkgLines)):
                if(packageTerm in pkgLines[i].lower()):

                    packageLine = pkgLines[i]

                    if(len(packageLine) > 8):

                        #print("extracting from line: " + packageLine)
                        lineParts = packageLine.split(" ")
                        nameParts = lineParts[0].split("/")

                        pkgInfo = {
                            "name": nameParts[0],
                            "installid": nameParts[0],
                            "version": lineParts[1],
                            "arch": lineParts[2],
                            "pkgmgr": self.name,
                            "description": "",
                        }
                        if(len(nameParts) > 1):
                            pkgInfo["spec"] = nameParts[1]

                        foundPkgInfos.append(pkgInfo)

        return foundPkgInfos

    def install(self,packageDef):
        command = "sudo apt-get install " + packageDef["installid"]
        print("Executing install: " + command)
        os.system(command)
        return True

from tabulate import tabulate
class UniStallManager:

    def __init__(self):
        self.packageManagers = []
        self.packageManagers.append(AptManager())
        self.packageManagers.append(SnapManager())
        self.packageManagers.append(FlatPakManager())

        self.tableKeys = ["name","version","pkgmgr","score","description"]
        self.tableLabels = ["Name","Version","Package Manager","Score","Description"]

    def find(self, fuzzyTerm):
        print("Trying to find package for: " + fuzzyTerm)

        searchTermHierarchy = createSearchHierarchy(fuzzyTerm)
        
        #scoreBoards = []

        fullScoreBoard = []

        for pkgManager in self.packageManagers:

            scoreBoard = createPkgScoreBoard(searchTermHierarchy, pkgManager)

            #nameResults = pkgManager.find(fuzzyTerm)
            #print("\nPackages found with " + pkgManager.name)
            #print(scoreBoard)

            #scoreBoards.push(scoreBoard)
            
            for scoreKey in scoreBoard:
                pkgInfo = scoreBoard[scoreKey]
                fullScoreBoard.append(pkgInfo)

        fullScoreBoard.sort(key=lambda pkgInfo: pkgInfo["score"],reverse=True)
        return fullScoreBoard

        """cnt = 0
        scoreTable = []
        for pkgScore in fullScoreBoard:
            scoreTable.append([str(cnt) + ")",pkgScore["name"],pkgScore["mgr"],pkgScore["score"]])
            cnt += 1

        #print(tabulate(scoreTable,headers=['Number', 'pkg-name', 'pkg-manager', 'score']))

        return scoreTable"""

        """for pkgScore in fullScoreBoard:

            print("\"" + pkgScore["name"] + "\"\t\t\t" + str(pkgScore["score"]) + "\t" + pkgScore["mgr"])
            ##print("\"" + pkgScore["name"] + "\": " + str(scoreBoard[key]))
            #sortedKeys = sorted(scoreBoard)
            #for key in sortedKeys:"""

    def promptInstall(self,scoreResults,maxShowCnt):
        print()
        #print(tabulate(scoreResults[0:maxShowCnt],headers=['Number', 'pkg-name', 'pkg-manager', 'score']))

        subListPkgInfos = scoreResults[0:maxShowCnt]
        printResults = []
        for row in subListPkgInfos:
            elem = []
            for propKey in self.tableKeys:
                elem.append(row[propKey])

            printResults.append(elem)

        print(tabulate(printResults,headers=self.tableLabels,showindex="always"))
        #print(tabulate(printResults,headers='keys',showindex="always"))
        if(len(scoreResults) > maxShowCnt):
            print("m) Show more")
        print("e) Exit")
        print()
        response = input("Which package to install? ")

        if(response.isnumeric()):
            pickedNumber = int(response)
            if(pickedNumber >= 0 and pickedNumber < maxShowCnt):
                return scoreResults[int(response)]
            else:
                print("Number not in range - try again")
                return self.promptInstall(scoreResults,maxShowCnt)

        elif(response == "m"):
            maxShowCnt = maxShowCnt * 5
            return self.promptInstall(scoreResults,maxShowCnt)

        elif(response == "e" or response == "exit"):
            return None

        else:
            return self.promptInstall(scoreResults,maxShowCnt)

    def findinstall(self,fuzzyTerm):
        fullScoreBoard = self.find(fuzzyTerm)
        maxShowCnt = 8

        packageToInstall = self.promptInstall(fullScoreBoard, maxShowCnt)

        if(packageToInstall is not None):
            #return self.installPkgDef({"name":packageToInstall[1],"mgr":packageToInstall[2]})
            return self.installPkgDef(packageToInstall)

        return False

    def getPackageManagerByName(self,name):
        for pkgMgr in self.packageManagers:
            if(pkgMgr.name == name):
                return pkgMgr

    def installPkgDef(self, pkgDefinintion):
        packageManager = self.getPackageManagerByName(pkgDefinintion["pkgmgr"])
        print("Installing " + pkgDefinintion["installid"] + " with " + packageManager.name)
        return packageManager.install(pkgDefinintion)
        #print("Installing")
        #print(str(pkgDefinintion))
        #return True

    def install(self, pkgName, pkgManager):
        print("Installing " + pkgName + " with " + pkgManager)
        return True

    def remove(self, pkgName):
        print("Trying to uninstall package: " + pkgName)


"""pkgManager = SnapManager()
results = pkgManager.find("firefox")
print(results)

pkgManager = AptManager()
results = pkgManager.find("firefox")
print(results)"""

pkgManager = UniStallManager()
#results = pkgManager.findinstall("Mozilla Firefox 75.0 (x64 de)")
#results = pkgManager.findinstall("notepad++")
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