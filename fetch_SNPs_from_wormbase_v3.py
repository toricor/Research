# -*- coding: utf-8 -*-
# set input/output file names!
# make an input file containing SNPs(WBVariation numbers) you need 

# File Name: fetch_SNPs_from_wormbase_v3.py(Old File Name:FetchSNPsFromWormBaseObjectOrientedCleaned.py)
# input: WBVariation Number (SNPs data)
# output: corresponding data from WormBase (Chromosome, physical pos., genetic pos., left flanking seq., 
# right flanking seq., is applicable the restriction enzyme

# ex. JU258, CB4856, ... : Strain Name
# ex. WS244: WormBase Data Version

import requests
import csv
import time

###############
input_filename  = 'sample_input_for_fetch_SNPs_from_wormbase_v3.csv'     #the file name of WBVariation numbers 
output_filename = 'sample_output_for_fetch_SNPs_from_wormbase_v3.csv'    #the result file
sleep_time = 0.3    # sec
###############

class WBVar:
    """
    If you want to fetch more data from WormBase, 
    read http://www.wormbase.org/about/userguide/for_developers/api-rest#01--10
    and  add and/or modify address below. Do not forget to add adequate methods to this class.  
    """
    fields = ['genomic_position', 'genetic_position', 'flanking_sequences', 'nucleotide_change']
    url_root = 'http://api.wormbase.org/rest/field/variation/'

    #example. wb = 'WBVar00000899'
    headers = {'content-type': 'application/json'}
    def __init__(self, wb):
        self.urls = []
        self.jsons = []
        self.wbvarnumber = wb
	
        self.physical_position = ''
        self.genetic_position = ''
        self.chromosome = ''
        self.left_flank = ''
        self.right_flank = ''
        self.wildtype = ''
        self.mutant = ''
	
    def set_valid_urls(self, wb, fields):
        for item in fields:
            self.urls.append(str(self.url_root) +str(wb) + "/" + str(item))
            		
    def fetch_json_data_from_wormbase(self, wb):
        headers = {'content-type': 'application/json'}
        for url in self.urls:
            self.jsons.append(requests.get(url, headers=headers).json())
		 
    def set_physical_position(self):
        ##ex. parse [u'II:14048668..14048668']
        h = str(self.jsons[0]['genomic_position']['data'][0]['label'].decode()).split(':')
        self.chromosome = h[0]
        self.physical_position = int(str(h[1].split('..')[0].decode()))
            
    def set_genetic_position(self):
        tmp = self.jsons[1]['genetic_position']['data'][0]['position']
        #ex. parse　[u'II:23.08 +/- 0.005 cM']  
        if tmp is not None:
            self.genetic_position = float(str(self.jsons[1]['genetic_position']['data'][0]['position'].decode()))
            
    def set_flanking_sequences(self):
        self.left_flank = self.jsons[2]['flanking_sequences']['data']['left_flank']
        self.right_flank = self.jsons[2]['flanking_sequences']['data']['right_flank']

    def set_nucleotide_change(self):    
        self.wildtype = self.jsons[3]['nucleotide_change']['data'][0]['wildtype']
        self.mutant = self.jsons[3]['nucleotide_change']['data'][0]['mutant']

    def get_count_of_r_enz_site(self, recog_seq, enz_name):
        '''return wt seq count, mut seq count and enzyme name'''
        wt_seq = (self.left_flank + self.wildtype + self.right_flank).upper()
        mut_seq = (self.left_flank + self.mutant + self.right_flank).upper()
        if self.left_flank == self.right_flank: # remove blank cells
            return (0,0,0)
        wt_count = 0
        mut_count = 0
        wt_count = wt_seq.count(recog_seq)
        mut_count = mut_seq.count(recog_seq)
        return wt_count, mut_count, enz_name

if __name__ == "__main__":
    error_log = {} # {"WBVar00000899": "Error Message"}

    f = open(input_filename,'rb') 
    g = open(output_filename,'wb')
    b = csv.reader(f)
    c = csv.writer(g)    	
    for row in b:
        # send requests and get json data
        # row[0] == WBVar00000899 or ['WBVar00000899']
        wbvarnumber = row[0].strip("'[]")
        variation = WBVar(wbvarnumber)
        variation.set_valid_urls(wbvarnumber, WBVar.fields)
        time.sleep(sleep_time) # do not send too many requests to the server per second
        try:            
            variation.fetch_json_data_from_wormbase(wbvarnumber)
        except:
            error_log[wbvarnumber] = 'Error requests.get()'
            continue
            
        # parse          
        try:
            variation.set_physical_position()
        except:
            error_log[wbvarnumber] = 'Error genomic_position'
            continue

        try:
            variation.set_genetic_position()
        except:
            error_log[wbvarnumber] = 'Error genetic_position' 
            continue
        
        try:
            variation.set_flanking_sequences()
        except:
            error_log[wbvarnumber] = 'Error flanking_sequences'
            continue
        
        try:
            variation.set_nucleotide_change()
        except:
            error_log[wbvarnumber] = 'Error nucleotide_change'
            continue
        
        # extract restriction enzyme sites
        r_enz_list = \
        [('CTCGAG','XhoI'),
         ('GAATTC','EcoRI'),
         ('CTGCAG','PstI'),
         ('GATATC','EcoRV'),
         ('TTTAAA','DraI'),
         ('CATATG','NdeI'),
         ('AAGCTT','HindIII')]

        r_enz_counts_list = []
        wt_count = mut_count = 0
        enzyme_name = ''
        try:
            for seq,enz in r_enz_list:
                wt_count, mut_count, enzyme_name = variation.get_count_of_r_enz_site(seq, enz)
                if wt_count == mut_count:
                    continue
                else:
                    r_enz_counts_list.append([wt_count, mut_count, enzyme_name])

            if  len(r_enz_counts_list)==0:   
                c.writerow([variation.wbvarnumber,
                    variation.chromosome,
                    variation.physical_position,
                    variation.genetic_position,
                    variation.left_flank,
                    variation.right_flank,
                    variation.wildtype,
                    variation.mutant])
            else:
                c.writerow([variation.wbvarnumber,
                    variation.chromosome,
                    variation.physical_position,
                    variation.genetic_position,
                    variation.left_flank,
                    variation.right_flank,
                    variation.wildtype,
                    variation.mutant,
                    r_enz_counts_list])
        except:
            continue

    if error_log:			
        print error_log
        
    f.close()
    g.close()
