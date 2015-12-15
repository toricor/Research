<i>C. elegans</i>の遺伝子と発現細胞を対応させる表を作成する。

##<a name="1">__geneID_to_expr_pattern.py__
  下記geneIDs.csvを入力としてwormbaseから各遺伝子の発現細胞情報を取得し、csvファイルを出力する。  
    **(Input)**geneIDs.csv  
        http://im-dev.wormbase.org/species/c_elegans/gene#2--10 より<i>C. elegans</i>のGene ID情報を取得した  
        c_elegans.PRJNA13758.current_development.functional_descriptions.txt  
    **(Output)**output_for_geneID_to_expr_pattern.csv or output_for_geneID_to_expr_pattern_no_extracomma.csv
        結果ファイル2種類（余計なコンマつき、及びそれを取り除いたもの）  
    **※restful_api_response_structure.csv**   
    response memo  
    
##<a name="2">**formating_geneID_to_expr_pattern.py**  
上記の結果ファイルを細胞（または組織）ごとに一行ずつに整形する。  
**(Input)**  output_for_geneID_to_expr_pattern(_no_extracomma).csv  
**(Output)** formatted_output_for_geneID_to_expr_pattern.csv
