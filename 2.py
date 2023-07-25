import json
import os
import pandas
from google.colab import drive

from google.colab import drive
drive.mount('/content/drive')

aggre_trans_path = "/content/drive/MyDrive/data/aggregated/transaction/country/india/"
aggre_trans_list = os.listdir(aggre_trans_path)
aggre_trans_year_wise = dict (categories=[], year=[], quarter=[], count=[], amount=[])
for year in range(len(aggre_trans_list)):
    print(year)
    json_path = aggre_trans_path+aggre_trans_list[year]+"/"
    print(json_path)

