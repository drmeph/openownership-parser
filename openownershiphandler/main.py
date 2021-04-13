import sys

from os import path

def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    print('File exists: '+ str(path.exists(sys.argv[1])))