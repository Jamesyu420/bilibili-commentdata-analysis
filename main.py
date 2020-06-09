from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.messagebox import *
from snownlp import SnowNLP
import os
from json.decoder import JSONDecodeError
from requests import get
from re import sub
from json import dump, loads
from time import localtime, strftime
import pandas as pd
import numpy as np
from jieba import load_userdict, lcut
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from sys import exit

flag: bool = True


def decode_json(r):
    try:
        response = r.json()
    except JSONDecodeError:
        # 虽然用的是requests的json方法，但要捕获的这个异常来自json模块
        return False
    else:
        return response


def check():
    scan = entry_msg.get()
    k = scan[0:2]
    if k == "BV" or "bv":
        return bv2av(scan)
    elif k == "AV" or "av":
        return scan[2:]
    else:
        exit(1)


def bv2av(bv):
    api = 'https://api.bilibili.com/x/web-interface/view'  # ?bvid=
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/80.0.3987.149 Safari/537.36'}
    r = get(api, {'bvid': bv}, headers=header)
    response = decode_json(r)
    try:
        print(str(response['data']['aid']))
        return str(response['data']['aid'])
    except (KeyError, TypeError):
        return False


def getCommentJson(aid):
    dict_data = {}
    date = []
    level = []
    text = []
    like = []
    j = 1
    while True:
        # noinspection PyBroadException
        try:
            url = "https://api.bilibili.com/x/reply?type=1&oid={0}&nohot=1&sort=0&pn={1}".format(aid, j)
            html = get(url)
            data = loads(html.text)
            for i in range(0, 20):  # 每页20条评论
                timeArray = localtime(data['data']['replies'][i]['ctime'])  # 时间戳
                date.append(strftime("%Y-%m-%d %H:%M:%S", timeArray))
                level.append(str(data['data']['replies'][i]['member']['level_info']['current_level']))  # 用户等级
                txt = data['data']['replies'][i]['content']['message']  # 评论内容
                txt = sub('\n', '', txt)
                txt = sub('\r', '', txt)
                text.append(txt)
                like.append(str(data['data']['replies'][i]['like']))  # 赞同数
            j += 1
        except Exception:
            break
    dict_data['date'] = date
    dict_data['level'] = level
    dict_data['text'] = text
    dict_data['like'] = like
    with open(r"data/commentdata.json", 'w', encoding='utf-8') as f:
        dump(dict_data, f, ensure_ascii=False)


def datapre(jsonfile=r"data/commentdata.json"):
    if flag:
        aid = check()
        # 由于b站反爬机制复杂而没找到可以调出视频名字的API接口，暂且搁置
        '''r = get("https://www.bilibili.com/video/" + aid, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'})
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser",from_encoding='gbk')
        Label(frm_under, text=soup.find('title').string, font=12).grid(ipadx=10, ipady=5, padx=20, pady=20)'''
        getCommentJson(aid)
    global df
    df = pd.read_json(jsonfile)
    df['cut'] = pd.Series(dtype=np.float64)
    for i in range(0, df.shape[0]):
        text = df['text'].iloc[i]
        txt_cut = lcut(text, cut_all=False)
        txt_cut = ' '.join(txt_cut)
        df['cut'].iloc[i] = txt_cut
    # data cleaning
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)


def wordcloud():
    global df
    series = df['cut']
    text_cut = ""
    for i in series:
        text_cut += i
    stop_words = open(r"data/stopwords.txt", encoding='utf-8').read().split('\n')
    background = Image.open(r"data/iconimage.png")
    graph = np.array(background)
    word_cloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", background_color="white", mask=graph,
                           stopwords=stop_words)
    word_cloud.generate(text_cut)
    plt.subplots(figsize=(12, 8))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig("clouds.png", dpi=300)
    plt.show()


def pie(data, ax):
    # 用户等级饼状图——视频受众分析
    x = data['level'].value_counts().sort_index(ascending=True)
    ax.pie(x, labels=list(x.index), startangle=180, shadow=True, autopct='%1.2f%%')
    ax.set(title="评论等级分布")
    ax.grid()


def scatter(data, ax):
    x = data['level'].sort_index(ascending=True)
    y = data['like'].sort_index(ascending=True)
    ax.scatter(x, y, marker='.')
    ax.set_title("等级——点赞散点图")
    ax.grid()


def timeseries(data, ax):
    # 评论等级时间序列图——谁在主导舆论？
    # 现存问题：时间序列没有同时兼容久远的视频和近期视频，显示效果不佳
    x = data['date']
    y = data['level']
    ax.plot_date(x, y, )
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(AutoDateLocator(maxticks=8))
    ax.legend(['评论'], loc='upper right')
    ax.set_title("用户等级时序分析")
    ax.set_ylabel("等级")
    ax.grid()


def draw():
    global df
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure("描述性图表分析")
    fig.set_size_inches(7, 7)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(212)
    pie(df, ax1)
    scatter(df, ax2)
    timeseries(df, ax3)
    plt.savefig("stats.png", dpi=300)
    plt.show()


def dataFind():
    root = Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    global flag
    flag = False
    datapre(filepath)
    flag = True


def feeling():
    global df
    df['sentiments'] = pd.Series(dtype=np.float64)
    df['result'] = pd.Series(dtype=str)
    for i in range(0, df.shape[0]):
        text = SnowNLP(df['text'].iloc[i])
        df['sentiments'].iloc[i] = text.sentiments
        if text.sentiments > 0.7:
            df['result'].iloc[i] = "积极"
        else:
            df['result'].iloc[i] = "消极"
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure("情感分析")
    fig.set_size_inches(6, 6)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    x = df['result'].value_counts().sort_index(ascending=True)
    ax1.pie(x, labels=list(x.index), startangle=180, shadow=True, autopct='%1.2f%%')
    ax1.set(title="情感分析饼状图")
    ax1.grid()
    p = df['date']
    q = df['result']
    ax2.plot_date(p, q)
    ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(AutoDateLocator(maxticks=8))
    ax2.legend(['评论'], loc='upper right')
    ax2.set_title("用户情感时序分析")
    ax2.set_ylabel("情感")
    ax2.grid()
    plt.savefig("sentiments.png", dpi=300)
    plt.show()


# 菜单栏
def aboutCall():
    showinfo(title="关于", message="独立完成人：余柏辰")


def helpCall():
    showinfo(title="功能介绍", message="输入任何一个b站视频地址(av号bv号均可)或导入json格式评论数据，进行数据分析并展示观众分布、评论态度与词云，旨在帮助用户对视频的影响有更深的认识。")


def whereCall():
    showinfo(title="文件目录", message=os.getcwd())


df = pd.DataFrame()
load_userdict(r"data/dict.txt")

window = Tk()
window.title("后浪入海——哔哩哔哩视频数据分析")
window.geometry("550x300+250+150")
frm = Frame(window)
frm.grid()
frm_top = Frame(frm)
frm_top.grid(row=0, column=0)
frm_bottom = Frame(frm)
frm_bottom.grid(row=1, column=0)
Label(frm_top, text="AV/BV号").grid(row=1, column=0, ipadx=10, ipady=5, padx=20, pady=20)
entry_msg = Entry(frm_top, width=40)
entry_msg.grid(row=1, column=1)
btn_Get = Button(frm_top, text="获取评论", command=datapre)
btn_Get.grid(row=1, column=3, ipadx=10, ipady=5, padx=20, pady=20)
btn_exist = Button(frm_bottom, text="导入数据", command=dataFind)
btn_exist.grid(row=1, column=1, ipadx=30, ipady=15, padx=20, pady=20)
btn_cloud = Button(frm_bottom, text="生成词云", command=wordcloud)
btn_cloud.grid(row=1, column=2, ipadx=30, ipady=15, padx=20, pady=20)
btn_analy = Button(frm_bottom, text="用户分析", command=draw)
btn_analy.grid(row=2, column=1, ipadx=30, ipady=15, padx=20, pady=20)
btn_feel = Button(frm_bottom, text="情感分析", command=feeling)
btn_feel.grid(row=2, column=2, ipadx=30, ipady=15, padx=20, pady=20)

menubar = Menu(window)
startmenu = Menu(menubar)
startmenu.add_command(label="目录", command=whereCall)
startmenu.add_command(label="退出", command=window.destroy)
menubar.add_cascade(label="文件", menu=startmenu)
helpmenu = Menu(menubar)
helpmenu.add_command(label="About", command=aboutCall)
helpmenu.add_command(label="说明", command=helpCall)
menubar.add_cascade(label="帮助", menu=helpmenu)
window.config(menu=menubar)
# 进入GUI
window.mainloop()
