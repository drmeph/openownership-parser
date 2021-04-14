import sys
import ijson
import json

from os import path
from types import SimpleNamespace
from .sqlFormatter import getInsert

def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    inputFile = sys.argv[1]
    print('Input File exists: '+ str(path.exists(inputFile)))

    outputFile = sys.argv[2]
    print('Output File exists: '+ str(path.exists(outputFile)))

    """Read Json file"""
    if not path.exists(inputFile):
        sys.exit('File does not exist!')

    if path.exists(outputFile):
        sys.exit('Output file already exists, please use another name of delete the file.')

    output = open(outputFile, "w+")

    with open(inputFile, 'r') as f:
        objects = ijson.items(f, 'item')

        for obj in objects:
            sobj = json.dumps(obj)
            jsonObj = json.loads(sobj, object_hook=lambda d: SimpleNamespace(**d))

            print("--- New Record ---")
            inserts = getInsert(jsonObj)
            output.write(inserts)

    output.close()