# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:00:52 2019

@author: pzhao

Process Buff Text File from raw pickle file, save as

"""

import os
import pickle
import pandas as pd


raw_path ='Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Buff'
save_path ='Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Buff'

# load file
with open(os.path.join(raw_path, 'buff_raw.p'),'rb') as f:
    raw_file = pickle.load(f)
    

content = [x for x, y in raw_file]
meta = [y for x, y in raw_file]

raw_df = pd.DataFrame( {'content': content, 'meta': meta})

# format content

def clean_content(string):  
    string = string.split('\n\n')
    string = map(lambda x : x.replace('\n',' ').replace('\t',' '), string)
    string = '\n'.join(string)
    
    return string

raw_df.content = raw_df.content.apply(clean_content)

## generate metadata of country and year from the original text
raw_df['country'] = raw_df.meta.apply(lambda x: x.split('\n')[-3].split('/')[-1])
raw_df.country.nunique() # 194 unique countries


## apply regular expression match to find date
raw_df['date']= raw_df.content.str.extract(r'(?P<ymd>[A-Z][a-z]*[ ][0-9]*[,][ ]*\d{4})')
raw_df['year'] = raw_df.date.astype(str).apply(lambda x: x[-4:])

# save resulte
raw_df.to_pickle(os.path.join(save_path, 'Buff_with_meta.pickle'))

# save some statistics
meta_df = raw_df[['country','year','date']]
meta_summary_df = pd.pivot_table(meta_df, values ='date', index ='country', columns ='year', aggfunc = len)
meta_summary_df.to_excel(os.path.join(save_path, 'meta_summary.xlsx'))