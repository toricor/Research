# Research
<i>C. elegans</i> research
##table of contents
**fetch_SNPs_from_wormbase_version.py** (use the latest version)  
fetching SNPs data from WormBase(http://www.wormbase.org/) and generating a csv file  

**extract_SNPs_of_a_wild_isolate.py**
extracting SNPs of a wild isolate you need from the file "WBVarNumbers_to_wild_isolates_WS244.csv"

**WBVarNumbers_to_wild_isolates_WS244.csv**  
A table of WBVariation Number to wild isolates　(the source code for generating this file is not uploaded)



**fetch_SNPs_from_wormbase_version.py** (最新版を使用のこと)    
WormBaseから特定のWBVar番号をもつSNP情報をダウンロードし、csvファイルにまとめる。制限酵素情報も付加する。
WBVar番号一覧のファイル(csvファイル)を作成し、入力とする。
・操作：入力ファイル名、出力ファイル名の指定(*.csv)　及び　HTTPリクエスト送信のインターバル時間指定(秒)

また、WormBase上の全WBVar情報とストレイン情報を対応させる表を作成した(WBVarNumbers_to_wild_isolates_WS244.csv, WS244のデータに基づく）。
 上記のcsvファイルに基づき、fetch~.pyプログラムで入力として用いるためのファイルを作成するプログラムを作成した。すなわち、特定のWild  IsolateがもつSNPsの一覧表csvファイルを作成するスクリプトを添付した(ExtractSNPsOfaWildIsolate.py)。




