# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 16:36:02 2019

@author: pzhao
"""

import pandas as pd
import numpy as np
import os
import re
import pickle
import matplotlib as plt

pd.set_option('display.max_colwidth', -1)


#%% 

data_folder = 'Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Topic'
ebv_file = open(os.path.join(data_folder, 'ebv_augmented_dict.p'), 'rb')
ebv_dict = pickle.load(ebv_file)

file_folder = 'Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Annotation'
doc_file = 'Authorities Views 20190703.xlsx'
doc_df =pd.read_excel(os.path.join(file_folder, doc_file))

#%%

for k, v in ebv_dict.items():
    
    pattern =  v['phrases'].replace('(','|').replace(')','|').replace('||','|').replace(' |','|').replace('| ', '|')

    pattern = (r'\b(' + pattern + r')\b').replace('|)',')').replace('(|','(')
    
    doc_df[k] = doc_df.paragraph.str.findall(pat = pattern, flags =re.IGNORECASE)
    
    doc_df[k +'_size'] = doc_df[k].apply(len)

    
#%%

doc_df.to_excel(os.path.join(data_folder, 'Authorities Views 20190703_with sector_augmented.xlsx'))
    
##re.findall(r'\b(?P<Title>gradual)' , t)
#pattern = r'(?P<' + 'Financial' +'>' + ebv_dict['Financial and Monetary Sector']['phrases'] + r')'
#pattern = pattern.replace('|)',')').replace('||','|')
#doc_df.paragraph.str.extract(pat = pattern, flags ='re.IGNORECASE', expand = False)

