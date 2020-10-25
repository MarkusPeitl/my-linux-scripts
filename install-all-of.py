import os
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser(description='Execute install command with text file package lines')
parser.add_argument('directorypath', help='Path to file containing package lines')

args = parser.parse_args()

directorypath = args.directorypath

for file in listdir(directorypath):
    #print("file: " + file)
    filename, file_extension = os.path.splitext(file)
    #print("file_extension: " + file_extension)
    filtePath = join(directorypath,file)
    if(isfile(filtePath) and file_extension == ".txt"):
        os.system("python3 install-pkg-list.py " + filtePath)

