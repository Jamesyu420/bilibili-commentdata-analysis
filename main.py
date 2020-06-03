from dataSort import *
from getCommentJson import *
from bv2av import *
from cloud import *
from dataanalysis import *


bv = str(input())
av = bv2av(bv)

getCommentJson(av)

df = datapre()
wordcloud(df['cut'])

draw(df)
