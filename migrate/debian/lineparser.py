import os.path

def getFilteredFileLines(path):
    if(os.path.isfile(path)):
        print(path + " is file")
        with open(path, "r", encoding="utf-8") as file:

            filteredLines = []

            for line in file:
                
                if(len(line) > 1 and line[0] != "#"):

                    line = line.replace("\n","")
                    line = line.lstrip(' ')
                    line = line.rstrip(' ')

                    filteredLines.append(line)

            return filteredLines

    return None