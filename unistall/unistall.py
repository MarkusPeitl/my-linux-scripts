import argparse
import os
import lineparser as lineparse

parser = argparse.ArgumentParser(description='Convert windows program names to debian apt packages')
parser.add_argument('filepath', help='Path to file containing the windows program names')
parser.add_argument('-c','--check', help='Path to file containing the windows program names')

args = parser.parse_args()

filepath = args.filepath

print(filepath)