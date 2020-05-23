import pandas as pd
import numpy as np
import jieba


def datapre(jsonfile="commentdata.json"):
    jieba.load_userdict("dict.txt")
    df = pd.read_json(jsonfile)
    df['cut'] = pd.Series()
    # data cleaning
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    for i in range(0, df.shape[0]):
        text = df['text'].iloc[i]
        txt_cut = jieba.lcut(text, cut_all=False)
        txt_cut = ' '.join(txt_cut)
        df['cut'].iloc[i] = txt_cut
    return df
