from os import listdir
from os.path import isfile, join
import sys 

def clean_zeros(dir_name):
    files = [join(dir_name, f) for f in listdir(dir_name) if isfile(join(dir_name, f))]
    values=[]
    for fn in files:
        with open(fn) as fd:
            for line in fd:
                pair = line.split(":")
                if (len(pair) < 2):
                    continue
                ni = int(pair[1]) 
                if (ni > 0):
                    values.append((pair[0], ni))
    values = sorted(values, key = lambda pair: pair[1], reverse=True)
    for v in values:
        print v[0],":",v[1]

def sort_results(dir_name):
    files = [join(dir_name, f) for f in listdir(dir_name) if isfile(join(dir_name, f))]
    values=[]
    for fn in files:
        with open(fn) as fd:
            for line in fd:
                pair = line.split(":")
                if len(pair) < 2:
                    continue
                ni = float(pair[1]) 
                if (ni > 0):
                    values.append((pair[0], ni))
    values = sorted(values, key = lambda pair: pair[1], reverse=True)
    for v in values:
        print v[0],":",v[1]

sort_results(sys.argv[1])

