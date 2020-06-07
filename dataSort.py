import pandas as pd
import numpy as np
from jieba import load_userdict,lcut


def datapre(jsonfile=r"data/commentdata.json"):
    load_userdict(r"data/dict.txt")
    df = pd.read_json(jsonfile)
    df['cut'] = pd.Series()
    # data cleaning
    df.drop_duplicates(inplace=True)
    #df.dropna(inplace=True)
    for i in range(0, df.shape[0]):
        text = df['text'].iloc[i]
        txt_cut = lcut(text, cut_all=False)
        txt_cut = ' '.join(txt_cut)
        df['cut'].iloc[i] = txt_cut
    return df
