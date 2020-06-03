import numpy as np
import pandas as pd
from snownlp import SnowNLP
from sklearn.model_selection import train_test_split

def snow_nlp(df):
    df['sentiment'] = pd.Series()
    for i in range(0,len(df)):
        df.iloc[i]['sentiment'] = SnowNLP(df.iloc[i]['text']).sentiments
