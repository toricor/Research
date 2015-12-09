# -*- coding: utf-8 -*-
import csv
import json

#######################################
input_filename  = 'strain_all_natural_isolates.json'                      #the file name of WBVariation numbers 
output_filename = 'wild_isolates.csv'         #the result file
#######################################

f = open(input_filename, 'rb') 
g = open(output_filename,'wb')
c = csv.writer(g)

json_data = json.load(f)
length = len(json_data["fields"]["natural_isolates"]["data"])
for i in xrange(length):
    elegans = json_data["fields"]["natural_isolates"]["data"][i]["species"]
    if elegans != "Caenorhabditis elegans":
        continue
    name    = json_data["fields"]["natural_isolates"]["data"][i]["strain"]["label"]
    c.writerow([name, elegans])

f.close()
g.close()