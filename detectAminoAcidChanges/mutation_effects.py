# -*- coding: utf-8 -*-
# python 3
# WBVar番号のリストファイルを読み込み、そのSNPが遺伝子のコード領域に含まれる場合、そのアミノ酸配列への影響を書き出す。
# 出力項目: WBVar番号、WB遺伝子番号、遺伝子名、染色体、物理的位置、クローン名（アイソフォーム名）、変異の効果、アミノ酸変異、エビデンスタイプ
# 
# リクエストを送るのはWBVar番号につき一回のみ
# 

import requests
import csv
import time
#import json #レスポンス整形のみ使用

f = open('WBVar_Strains_JU258.csv','r') #読み込むcsvファイル名
g = open('mutation_effects_JU258.csv','w', newline='')  #書き込むcsvファイル名（上書き）
b = csv.reader(f)
c = csv.writer(g)

url_1 = 'http://api.wormbase.org/rest/field/variation/'
field1 = '/'+'features_affected'

#csvファイルからwb番号読み出し。
#WBVar番号は一番左のカラムへ配置しておくこと
for num in b:  
    #num[0]は['WBVar00000899']
    wb = num[0].strip("'[]")
    val_url1= url_1 + wb + field1
    
    #HTTPレスポンスget
    try:
        headers = {'content-type': 'application/json'}
        time.sleep(0.5)
        r1 = requests.get(val_url1, headers=headers)
    except:
        print [wb,'Error requests.get()']
        continue
    #json        
    r_list=[]; r_list = [r1]
    if all(k.status_code == 200 for k in r_list):
        q1 = r1.json()
        
        #ここからparseする
        try:
            gene_id = q1["features_affected"]["data"]["Gene"][0]["id"]
            gene_label = q1["features_affected"]["data"]["Gene"][0]["label"]
            chromosome = q1["features_affected"]["data"]["Chromosome"][0]["label"]
            genomic_position = q1["features_affected"]["data"]["Chromosome"][0]["start"]
            #print(gene_id, gene_label, chromosome, genomic_position)
            Predicted_cds = q1["features_affected"]["data"]["Predicted_CDS"]
            for i in range(len(Predicted_cds)):
                protein_effects_dic = q1["features_affected"]["data"]["Predicted_CDS"][i]["protein_effects"]
                clone_label = Predicted_cds[i]["label"]    
                effect_type  = list(protein_effects_dic.keys())[0]
                amino_change = protein_effects_dic[effect_type]["description"]
                evidence_type = protein_effects_dic[effect_type]["evidence_type"]
                result_for_a_isoform_list = [clone_label, effect_type, amino_change, evidence_type]
                print(wb, chromosome, gene_label, result_for_a_isoform_list)
                data_list = [wb, gene_id, gene_label, chromosome, genomic_position] + result_for_a_isoform_list
                c.writerow(data_list)
                
        except:
            #print([wb])
            continue
        
    #status_codeが 200(正常)ではなかった場合:     
    else:
        print [wb, r1.status_code] 
        
g.flush()
f.close(); g.close()
