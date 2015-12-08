import requests
import json

headers = {'content-type': 'application/json'}
gene_number = "WBGene00004224"
url = "http://www.wormbase.org/rest/widget/gene/" + gene_number + "/expression"
data = requests.get(url, headers=headers).json()
#print json.dumps(data["fields"]["expression_patterns"]["data"][0]["expressed_in"], indent=4)
parsed = data["fields"]["expression_patterns"]["data"][0]["expressed_in"]
expr_cells = []
for item in parsed:
    expr_cells.append(item["label"])
print expr_cells