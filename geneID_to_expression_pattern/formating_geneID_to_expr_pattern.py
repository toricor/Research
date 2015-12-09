# -*- coding: utf-8 -*-
import csv

#######################################
input_filename  = 'output_for_geneID_to_expr_pattern.csv'                      #the file name of WBVariation numbers 
output_filename = 'formatted_output_for_geneID_to_expr_pattern.csv'         #the result file
#######################################

f = open(input_filename, 'rb') 
g = open(output_filename,'wb')
b = csv.reader(f)
c = csv.writer(g)

for row in b:
    gene_id = row[0]
    gene = row[1]
    ref = row[2]
    comment = row[3]
    sites = row[4:]
    for site in sites:
        if not site:
            break
        c.writerow([gene_id, gene, site, ref, comment])

f.close()
g.close()