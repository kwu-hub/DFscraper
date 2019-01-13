import json
import sys
from collections import defaultdict
from os import listdir
from os.path import isfile, join

directory = sys.argv[1]

files = [f for f in listdir(directory) if isfile(join(directory, f))]

all_data = defaultdict(list)
for f in files:
    if ".json" in f:
        path = directory + "/" + f
        with open(path) as p:
            data = json.load(p)
            for k in data.keys():
                all_data[k].append(data[k])
with open(directory + '/All'+str(sys.argv[1])+'.json', 'w') as outfile:
    json.dump(all_data, outfile)
exit()
