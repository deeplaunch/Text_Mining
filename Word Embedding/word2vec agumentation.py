# -*- coding: utf-8 -*-
"""
Spyder Editor

This file uses pre-trained w2v model to augment the EBV list

"""

import os
import pickle
import pandas as pd
from gensim.models import Word2Vec
#from nltk.tokenize import word_tokenize, sent_tokenize
#import gensim


def get_most_similar(phrs, model):
    
    if phrs in model.wv.vocab:
        # If the entire phrase is in the model's dictionary, get most simiilar
        return model.wv.most_similar(phrs)
    else:
        # If the phrase can't be found in the model's dictionary        
        word_ls = phrs.split('_')
        word_ls = [w for w in word_ls if w in model.wv.vocab] ## find out words in dictioary
        if len(word_ls) ==0: # None of the words are in the dictionary
            return [] 
        v_ls = [model.wv.get_vector(w) for w in word_ls]
        v = sum(v_ls) ## calcualte sum of vector
        return model.wv.similar_by_vector(v)

#1. load pre-trained imf w2v model
model_path = os.path.join('../model','imf_160.w2v')
imf_w2v = Word2Vec.load(model_path)

#2. load the original EBV dictionary
data_folder = '../data'
ebv_file = open(os.path.join(data_folder, 'ebv_dict.p'), 'rb')
ebv_dict = pickle.load(ebv_file)
ebv_dict = {k.lower(): v for k, v in ebv_dict.items() if len(k)>0 and v != 'Economic Theory and Research'}

ebv_df = pd.DataFrame(data={'phrases': list(ebv_dict.keys()), 'category': list(ebv_dict.values())})
ebv_df['phrases_annotated'] = ebv_df.phrases.str.replace(' ','_')

#3. create list of most similar words
ebv_df['most_similar'] = ebv_df.phrases_annotated.apply(get_most_similar, model= imf_w2v)
ebv_df['most_similar'] = ebv_df.most_similar.apply(lambda l: ','.join([x for x , y in l]))

#4. save output
ebv_df.to_excel('../data/augmented_ebv.xlsx')