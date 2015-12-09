# coding:utf-8
# extract_SNPs_of_a_wild_isolate.py
# 選択したStrainがもつWBVar番号をcsv書き出し

import csv

##########################
strain_name = "CB4852"     # 抽出したいwild isolateのストレイン名
##########################

f = open("WBVarNumbers_to_wild_isolates_WS244_ref.csv", "rb") # input_filename
g = open("WbVarNumToWildIsolate_"+strain_name + ".csv", "wb") #　output_filename
c = csv.reader(f)
d = csv.writer(g)

for wb in c:
    wb_list = []
    strain_list = []
    wb_list = wb[0]
    strain_list = wb[1]
    if strain_name in strain_list:
        d.writerow((wb_list.strip("[']"),))
f.close()
g.close()