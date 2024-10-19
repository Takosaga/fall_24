#!/usr/bin/env python3

# for interacting with the interpreter
import sys

# for input stream to python read line by line
for line in sys.stdin:
    # line stips ends
    line = line.strip()
    # value gets into two variables of city and temp
    city,temp = line.split(',')

    try:
        temp = float(temp) # try to convert temp to a float
        print('%s\t%s' % (city, temp))
    except ValueError:
        continue # if temp cant be converted then continue
