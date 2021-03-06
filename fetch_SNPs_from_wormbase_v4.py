# -*- coding: utf-8 -*-
# FetchSNPsFromWormBaseObjectOriented.py
# input: WBVariation Number (SNPs data)
# output: corresponding data from WormBase (Chromosome, physical pos., genetic pos., left flanking seq., 
# right flanking seq., is applicable the restriction enzyme

# JU258: Strain Name
# WS244: WormBase Data Version

class WBVar:
    """
    If you want to fetch more data from WormBase, 
    read http://www.wormbase.org/about/userguide/for_developers/api-rest#01--10
    and  add and/or modify address below. Do not forget to add adequate methods.  
    """
    fields = ['genomic_position', 'genetic_position', 'flanking_sequences', 'nucleotide_change', 'overview']
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
        self.other_name = ''
	
    def set_valid_urls(self, wb, fields):
        for item in fields:
            #print str(self.url_root) +str(wb) + "/" + str(item)
            self.urls.append(str(self.url_root) +str(wb) + "/" + str(item))
            		
    def fetch_json_data_from_wormbase(self, wb):
        try:
            headers = {'content-type': 'application/json'}
            for url in self.urls:
                self.jsons.append(requests.get(url, headers=headers).json())
        except:
            print wb, "Error requests.get()"
		 
    def set_physical_position(self):
        try:
            ##ex. parse [u'II:14048668..14048668']
            h = str(self.jsons[0]['genomic_position']['data'][0]['label'].decode()).split(':')
            self.chromosome = h[0]
            self.physical_position = int(str(h[1].split('..')[0].decode()))
        except:
            error_log[self.wbvarnumber] = 'Error genomic_position'
            
    def set_genetic_position(self):
        try:        
            tmp = self.jsons[1]['genetic_position']['data'][0]['position']
            #ex. parse　[u'II:23.08 +/- 0.005 cM']  
            if tmp is not None:
                self.genetic_position = float(str(self.jsons[1]['genetic_position']['data'][0]['position'].decode()))
        except:
            error_log[self.wbvarnumber] = 'Error genetic_position' 
            
    def set_flanking_sequences(self):
        try: 
            self.left_flank = self.jsons[2]['flanking_sequences']['data']['left_flank']
            self.right_flank = self.jsons[2]['flanking_sequences']['data']['right_flank']
        except:
            error_log[self.wbvarnumber] = 'Error flanking_sequences'

    def set_nucleotide_change(self):    
        try:
            self.wildtype = self.jsons[3]['nucleotide_change']['data'][0]['wildtype']
            self.mutant = self.jsons[3]['nucleotide_change']['data'][0]['mutant']
        except:
            error_log[self.wbvarnumber] = 'Error nucleotide_change'
    
    def set_other_name(self):
        try:
            ls = []
            for item in self.jsons[4]['overview']['other_names']['data']:
                ls.append(str(item.decode()))
            self.other_name = ls
        except:
            error_log[self.wbvarnumber] = 'Error other_name'

    def get_count_of_r_enz_site(self, recog_seq, enz_name):
        '''return wt seq count, mut seq count and enzyme name'''
        wt_seq = (self.left_flank + self.wildtype + self.right_flank).upper()
        mut_seq = (self.left_flank + self.mutant + self.right_flank).upper()
        if self.left_flank == self.right_flank: # remove blank cells
            return None
        wt_count = 0
        mut_count = 0
        wt_count = wt_seq.count(recog_seq)
        mut_count = mut_seq.count(recog_seq)
        return wt_count, mut_count, enz_name

if __name__ == "__main__":
    import requests
    import csv
    import time
    error_log = {} # {"WBVar00000899": "Error Message"}

    ###############
    input_filename = 'WBVar_Strains_CB4856.csv'             #WBVar.Num. file name
    output_filename = 'CB4856_WS244_v4.csv' 	    
    ###############

    f = open(input_filename,'rb') 
    g = open(output_filename,'wb')
    b = csv.reader(f)
    c = csv.writer(g)    
    c.writerow(['WBVarNumber','Chromosome','physical position','genetic position','left flanking',
    'right flanking','wildtype','mutant','enzyme', 'other name'])	
    for row in b:
        # send requests and get json data
        # row[0] == WBVar00000899 or ['WBVar00000899']
        wbvarnumber = row[0].strip("'[]")
        variation = WBVar(wbvarnumber)
        variation.set_valid_urls(wbvarnumber, WBVar.fields)
        #################
        time.sleep(0.5) # do not send too many requests to the server per second
        #################
        variation.fetch_json_data_from_wormbase(wbvarnumber)

        # parse          
        variation.set_physical_position()  
        variation.set_genetic_position()
        variation.set_flanking_sequences()
        variation.set_nucleotide_change()
        variation.set_other_name()

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
        for seq,enz in r_enz_list:
            wt_count, mut_count, enzyme_name = variation.get_count_of_r_enz_site(seq, enz)
            if wt_count == mut_count:
                continue
            else:
                r_enz_counts_list.append([wt_count, mut_count, enzyme_name])
        c.writerow([variation.wbvarnumber,
                    variation.chromosome,
                    variation.physical_position,
                    variation.genetic_position,
                    variation.left_flank,
                    variation.right_flank,
                    variation.wildtype,
                    variation.mutant,
                    r_enz_counts_list,
                    variation.other_name])

    if error_log:			
        print error_log
    f.close(); g.close()
