# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:00:52 2019

@author: pzhao

Process Buff Text File from raw pickle file, save data and stats in pandas dataframe

"""

import os
import pickle
import pandas as pd
import re


def load_file(raw_path, file_name ='buff_raw.p'):
    '''load file'''
    with open(os.path.join(raw_path, file_name),'rb') as f:
        raw_file = pickle.load(f)
        
    content, meta, file_name = zip(*raw_file)
    df = pd.DataFrame( {'content': content, 'meta': meta, 'file_name': file_name})
    
    return df

def drop_duplicates(df):
    
    '''remove duplicate files by using the revised version'''
    df['short_name'] = df.file_name.str.rsplit('\\').apply(lambda x: x[-1]).str.strip('.txt')
    df['left_name'] = df.short_name.str.split('_').apply(lambda x: '_'.join(x[0:4]))
    df['version'] = df.short_name.str.split('_').apply(lambda x: x[-1] if re.search(r'[a-z]', x[-1]) is not None else None)
        #raw_df.version.value_counts()
    df = df.fillna('Rev0').sort_values(['left_name','version']).groupby('left_name').last()    
    return df
    #raw_df.version.value_counts()

def clean_content(string):  
    '''format content'''
    string = string.split('\n\n')
    string = map(lambda x : x.replace('\n',' ').replace('\t',' '), string)
    string = '\n'.join(string)
    
    return string
    
def add_country(df):
    ''' add yaer'''
        
    ## generate metadata of country and year from the original text
    df['country'] = df.meta.apply(lambda x: x.split('\n')[-3].split('/')[-1])
    df.country.nunique() # 194 unique countries
        
    # special treatment of nan
    df.loc[df.country =='', 'country']= df[df.country ==''].meta.str.extract(r'on ([\w|\s|\-|\'|\.|\;|\(|\|,)]*)[ ][\-]*[ ][Executive Board Meeting|EBM\/|EBM\\]').loc[:,0]
    df.loc[df.country.isna(), 'country']= df[df.country.isna()].meta.str.extract(r'on ([\w|\s|\-|\'|\.|\;|\(|\|,)]*)\sExecutive Board Meeting').loc[:,0].to_list()
    
    # filter out na
    print('Dropping {} row with missing country'.format(df.country.isna().sum()))
    df = df[~df.country.isna()]
    
    return df

def add_year(df):
    
    '''apply regular expression match to find date'''
    df['date']= df.content.str.extract(r'(?P<ymd>[A-Z][a-z|\s]*[ ][0-9]*[\,|\.][ ]*\d{4})')
    df['year'] = df.date.astype(str).apply(lambda x: x[-4:])
    print('Dropping {} row with missing English date'.format(df.date.isna().sum()))
    df = df[~df.date.isna()]
    
    return df

def save_result(df, save_path, save_name = 'Buff_with_meta.pickle'):
    '''save resulte'''
    
    df.to_pickle(os.path.join(save_path, save_name))
    
    return None

def save_stats(df, save_path, save_name ='meta_summary.xlsx'):
    '''save some statistics'''
    meta_df = df[['country','year','date']]
    meta_summary_df = pd.pivot_table(meta_df, values ='date', index ='country', columns ='year', aggfunc = len)
    meta_summary_df.to_excel(os.path.join(save_path, 'meta_summary.xlsx'))
    
    return None


if __name__=='__main__':
        
    raw_path ='Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Buff'
    save_path ='Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Buff'
    
    raw_df = load_file(raw_path=raw_path)
    new_df = drop_duplicates(raw_df)    
    new_df.content = new_df.content.apply(clean_content)
    new_df = add_country(new_df)
    new_df = add_year(new_df)
    save_result(new_df, save_path=save_path)
    save_stats(new_df, save_path= save_path)