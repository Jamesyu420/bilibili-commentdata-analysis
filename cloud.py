from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def wordcloud(series):
    text_cut = ""
    for i in series:
        text_cut += i
    stop_words = open("stopwords.txt", encoding='utf-8').read().split('\n')
    background = Image.open("iconimage.png")
    graph = np.array(background)
    # 现在存有问题：如果设置背景图，则输出词云图极不清晰
    word_cloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", background_color="white", mask=graph,
                           stopwords=stop_words)
    word_cloud.generate(text_cut)
    plt.subplots(figsize=(12, 8))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig("clouds.png",dpi=300)
    plt.show()
