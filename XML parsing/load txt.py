# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:39:04 2019

@author: pzhao

Load Buff Text File from original folder, Save as Pickle

"""

import os
import pickle

path = '\\\\Appbwn01d\\IR\\BUFF\\EXTRACT'
save_path ='Q:\DATA\SPRMP\CSR_Coordination\Traction\Sentiment analysis\data\Buff'


## get all text files
files = []

for r, d, f in os.walk(path): # r=root, d=directories, f = files
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

buff_files =[f for f in files if 'record' not in f]      

## build a list, each element for loading every file as tuple with (content, metadata)
oput =[]

for f in buff_files:
    ## load document
    with open(f, encoding="utf8") as file:
        content = file.read()
    ## load metadata file    
    b = '\\'.join(f.split('\\')[:-1]) + '\\record.txt'
    with open(b, encoding="utf8") as file:
        meta = file.read()

    oput.append((content, meta))
    
## save tuple list as raw pickle file  
with open(os.path.join(save_path, 'buff_raw.p'),'wb') as f:
    pickle.dump(oput, f)