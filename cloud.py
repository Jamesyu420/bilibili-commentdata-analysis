from wordcloud import WordCloud
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def wordcloud(series):
    text_cut = ""
    for i in series:
        text_cut += i
    stop_words = open("stopwords.txt", encoding='utf-8')
    background = Image.open("book.jpg")
    # wordcloud主要问题在于背景图的形状没有解决
    graph = np.array(background)
    word_cloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", background_color="white", mask=graph,
                           stopwords=stop_words)
    word_cloud.generate(text_cut)
    plt.subplots(figsize=(12, 8))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
