import csv
import requests
#import json
import time

#######################################
input_filename  = 'geneIDs_latter.csv'       #the file name of WBVariation numbers 
output_filename = 'output_for_geneID_to_expr_pattern_latter.csv'    #the result file
sleep_time = 0.0                      # sec
#######################################

f = open(input_filename, 'rb') 
g = open(output_filename,'wb')
b = csv.reader(f)
c = csv.writer(g)

for row in b:
    headers = {'content-type': 'application/json'}
    gene_ID = row[0]
    url = "http://www.wormbase.org/rest/widget/gene/" + gene_ID + "/expression"
    try:
        time.sleep(sleep_time)
        data = requests.get(url, headers=headers).json()
    except:
        continue
    gene = data["fields"]["name"]["data"]["label"]
    
    #print json.dumps(data["fields"]["expression_patterns"]["data"][0]["expressed_in"], indent=4)
    tmp_parsed = data["fields"]["expression_patterns"]["data"]
    if not tmp_parsed:
        continue
    for i in xrange(len(tmp_parsed)):
        try:
            cells = [dic["label"] for dic in tmp_parsed[i]["expressed_in"]]
        except:
            cells = ""
        try:
            ref   = tmp_parsed[i]["description"]["evidence"]["Reference"]["label"]
        except:
            ref   = ""
        try:    
            com   = tmp_parsed[i]["description"]["text"]
        except:
            com   = ""
            
        result = [gene_ID, gene, ref, com]
        for cell in cells:
            result += [cell]
        c.writerow(result)

f.close()
g.close()