# -*- coding: utf-8 -*-
# FetchSNPsFromWormBase.py
# """detect SNPs for SNPs-mapping"""
# input: WBVariation Number (SNPs data, csv file)
# output: corresponding data from WormBase (Chromosome, physical pos., genetic pos., left flanking seq., 
# right flanking seq., is applicable the restriction enzyme  (csv file)

# JU258: Strain Name
# WS244: WormBase Data Version

import requests
import csv
import time
#import json

def get_count_of_r_enz_site(recog_seq, enz_name):
    '''return wt seq count, mut seq count and enzyme name'''
    wt = 0
    mut = 0
    wt = wt_seq_upper.count(recog_seq)
    mut = mut_seq_upper.count(recog_seq)
    return wt, mut, enz_name

input_filename = 'WBVarNum_JU258.csv' #WBVar.Num. file name
output_filename = 'SNPsData_WS244_JU258.csv' #output file name

f = open(input_filename,'rb') 
g = open(output_filename,'wb')
b = csv.reader(f)
c = csv.writer(g)

"""If you want to fetch more data from WormBase, 
read http://www.wormbase.org/about/userguide/for_developers/api-rest#01--10
and  add and/or modify address below. """

url1 = 'http://api.wormbase.org/rest/field/variation/'
field1 = '/'+'genomic_position'
field2 = '/'+'genetic_position'
field3 = '/'+'flanking_sequences'
field4 = '/'+'nucleotide_change'

error_log = {} # {"WBVar00000899": "Error Message"}
for num in b:  
    #num[0] == WBVar00000899 or ['WBVar00000899']
    wb = num[0].strip("'[]")
    val_url1= url1 + wb + field1
    val_url2= url1 + wb + field2  
    val_url3= url1 + wb + field3
    val_url4= url1 + wb + field4

    try:
        #################
        time.sleep(0.5) # do not send too many requests to the server per second
        #################
        headers = {'content-type': 'application/json'}
        res1 = requests.get(val_url1, headers=headers)
        res2 = requests.get(val_url2, headers=headers)
        res3 = requests.get(val_url3, headers=headers)
        res4 = requests.get(val_url4, headers=headers)
    except:
        #print wb,'Error requests.get()'
        error_log[wb] = 'Error requests.get()'
        continue
        
    #json        
    res_list = [res1, res2, res3, res4]
    if all(k.status_code == 200 for k in res_list):
        q1 = res1.json();      q2 = res2.json()
        q3 = res3.json();      q4 = res4.json()
        
        # parse        
        #################################################   
        #1 parse genomic_position　
        dic1 ={}; genomic_position_list = []
        chr_list = []; physical_pos = []
        try:
            dic1 = q1['genomic_position']['data'][0]     
            genomic_position_list.append(dic1['label']) 
            ##ex.  parse [u'II:14048668..14048668']
            chr1 = genomic_position_list[0]
            h = chr1.split(':')
            chr_list.append(h[0])
            physical_pos.append(h[1].split('..')[0])
        except:
            #print wb,'Error genomic_position'
            error_log[wb] = 'Error genomic_position'
            continue
        
        #2 parse genetic_position  
        dic2 = {} ; genetic_position_list = [] 
        genetic_num_list = []
        try:
            dic2 = q2['genetic_position']['data'][0]  
            genetic_position_list.append(dic2['formatted'])
            #ex. parse　[u'II:23.08 +/- 0.005 cM']  
            if genetic_position_list[0] is not None:
                chr2 = genetic_position_list[0]
                h2 = chr2.split(':')
                string = h2[1].split('+')[0]
                genetic_num_list.append(h2[1].split('+')[0])
        except:
            #print wb,'Error genetic_position'
            error_log[wb] = 'Error genetic_position'
            continue
            
        #3 parse flanking_sequences: left&right flank
        dic3 ={} 
        left_seq = []; right_seq = []
        try: 
            dic3 = q3['flanking_sequences']['data']   
            left_seq.append(dic3['left_flank'])
            right_seq.append(dic3['right_flank'])
        except:
            #print wb,'Error flanking_sequences'
            error_log[wb] = 'Error flanking_sequences'
            continue

        #4 parse nucleotide_change: WT and mutant
        dic4 ={}
        wildtype =[]; mutant = []
        try:
            dic4 = q4['nucleotide_change']['data'][0]
            wildtype.append(dic4['wildtype'])
            mutant.append(dic4['mutant'])
        except:
            #print wb,'Error nucleotide_change' 
            error_log[wb] = 'Error nucleotide_change'
            continue

        data_list = []
        data_list = [wb, chr_list, physical_pos, genetic_num_list,
        left_seq[0], right_seq[0],wildtype[0],mutant[0]]
        
        ################################################################
        # apply restriction enzymes
        wt_seq = []; mut_seq = [] 
        wt_seq_upper =[]; mut_seq_upper=[]
        if left_seq[-1] == right_seq[-1]: # remove blank cells
            data_list.append('')
            c.writerow(data_list)
            continue
        else:
            try:
                #wt_seq = left_seq + mutation + right_seq
                wt_seq=data_list[4]+data_list[6]+data_list[5]   
                mut_seq=data_list[4]+data_list[7]+data_list[5]  
            except:
                #print wb, 'Error wt/mut_seq'
                error_log[wb] = 'Error wt/mut_seq'
                continue
                
            wt_seq_upper = wt_seq.upper()
            mut_seq_upper= mut_seq.upper()
            
            r_enz_list = \
            [('CTCGAG','XhoI'),
             ('GAATTC','EcoRI'),
             ('CTGCAG','PstI'),
             ('GATATC','EcoRV'),
             ('TTTAAA','DraI'),
             ('CATATG','NdeI')]
            r_enz_counts_list = []
            wt = mut = 0; enz =""
            for seq,enz in r_enz_list:
                wt,mut,enz = get_count_of_r_enz_site(seq, enz)
                if wt == mut:
                    continue
                else:
                    r_enz_counts_list.append([wt, mut, enz])
            data_list.append(r_enz_counts_list)
            c.writerow(data_list)
    
    else: # status_code != 200  
        print wb,res1.status_code,res2.status_code, res3.status_code, res4.status_code

print error_log
f.close(); g.close()
