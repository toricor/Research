# -*- coding: utf-8 -*-
# wild_isolate_and_SNPcount.py

import csv
import requests
#import json
import time

#######################################
input_filename  = 'wild_isolates_celegans.csv'             #the file name of WBVariation numbers 
output_filename = 'wild_isolate_and_snp_count.csv'         #the result file
sleep_time = 0.5                      # sec
#######################################

f = open(input_filename, 'rb') 
g = open(output_filename,'wb')
b = csv.reader(f)
c = csv.writer(g)

for row in b:
    strain = row[0]
    url = "http://www.wormbase.org/rest/widget/strain/" + strain + "/contains"
    headers = {'content-type': 'application/json'}
    try:
        time.sleep(sleep_time)
        data = requests.get(url, headers=headers).json()
    except:
        continue
    
    try:
        count = data["fields"]["alleles"]["data"].split()[0].encode()
    except:
        count = None 
        
    c.writerow([strain, count])
    
f.close()
g.close()