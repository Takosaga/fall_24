#!/usr/bin/env python3

import sys

# for counters for citys
current_city = None
current_sum = 0
current_count = 0

for line in sys.stdin:
    line = line.strip()
    city, temp = line.split('\t',1) # since a tab was used in mappers, uses it as delimiter
    try:
        temp = float(temp)
    except ValueError:
        continue # double sanity check to see temp is a float

    if current_city == city:
        #counting
        current_sum += temp
        current_count += 1
    else:
        if current_city:
            # Output the avg temp for the current city
            print('%s\t%s'%(current_city,current_sum/current_count))
        #if not current city then current city changes
        current_city = city
        current_sum = temp
        current_count = 1

# output the average temp for the last city
if current_city == city:
    print('%s\t%s' % (current_city, current_sum / current_count))
