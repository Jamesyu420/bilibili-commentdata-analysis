import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter


def pie(df, ax):
    # 用户等级饼状图——视频受众分析
    x = df['level'].value_counts().sort_index(ascending=True)
    ax.pie(x, labels=list(x.index), startangle=180, shadow=True, autopct='%1.2f%%')
    ax.set(title="评论等级分布")
    ax.grid()

def scatter(df,ax):
    x = df['level'].sort_index(ascending=True)
    y = df['like'].sort_index(ascending=True)
    ax.scatter(x,y,marker='.')
    ax.set_title("等级——点赞散点图")
    ax.grid()

def timeseries(df, ax):
    #评论等级时间序列图——谁在主导舆论？
    #现存问题：时间序列没有同时兼容久远的视频和近期视频，显示时效果不佳
    x = df['date']
    y = df['level']
    ax.plot_date(x, y,)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(AutoDateLocator(maxticks=8))
    ax.legend(['评论'], loc='upper right')
    ax.set_title("用户等级时序分析")
    ax.set_ylabel("等级")
    ax.grid()


def draw(df):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure("描述性图表分析")
    fig.set_size_inches(7,7)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(212)
    pie(df, ax1)
    scatter(df,ax2)
    timeseries(df, ax3)
    plt.show()
