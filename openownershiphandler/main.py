import sys
import ijson

from os import path

def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    inputFile = sys.argv[1]
    print('File exists: '+ str(path.exists(inputFile)))

    """Read Json file"""
    if not path.exists(inputFile):
        sys.exit('File does not exist!')

    with open(inputFile, 'r') as f:
        objects = ijson.items(f, 'item')

        for obj in objects:
            print(obj)
