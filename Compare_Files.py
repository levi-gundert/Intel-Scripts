#!/usr/local/bin/env python

'''

Identify lines in common and count their frequency across multiple files within a user defined directory

'''

import os
import collections
import operator
import argparse
from pprint import pprint

# user defined directory containing multiple files
parser = argparse.ArgumentParser(description="provide the input directory")
parser.add_argument('--directory', '-d', help="full path input directory location", required=True)
args = parser.parse_args()

# open all files in directory
filenames = os.listdir(args.directory)
files = [open(name).readlines() for name in filenames]

# for loop magic
sets = [set(line.strip() for line in file)
        for file in files]

# count line commonality
combined_counter = reduce(operator.add, [collections.Counter(s) for s in sets])

# print the 50 most common lines and their respective frequency
pprint(combined_counter.most_common(50))
