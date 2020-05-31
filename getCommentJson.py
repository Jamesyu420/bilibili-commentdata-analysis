from re import sub
from requests import get
from json import dump, loads
from time import localtime,strftime

def saveCommentJson(filename,dict_data):
    with open(filename,'w',encoding='utf-8') as f:
        dump(dict_data,f,ensure_ascii=False)
def getCommentJson(aid):
    dict_data = {}
    date = []
    level = []
    text = []
    like = []
    j = 1
    while(True):
        try:
            url = "https://api.bilibili.com/x/reply?type=1&oid={0}&nohot=1&sort=0&pn={1}".format(aid,j)
            html = get(url)
            data = loads(html.text)
            for i in range(0,20):   #每页20条评论
                timeArray = localtime(data['data']['replies'][i]['ctime'])     #时间戳
                date.append(strftime("%Y-%m-%d %H:%M:%S",timeArray))
                level.append(str(data['data']['replies'][i]['member']['level_info']['current_level']))    #用户等级
                txt = data['data']['replies'][i]['content']['message']     #评论内容
                txt = sub('\n','',txt)
                txt = sub('\r','',txt)
                text.append(txt)
                like.append(str(data['data']['replies'][i]['like']))      #赞同数
            j += 1
        except:
            break
    dict_data['date'] = date
    dict_data['level'] = level
    dict_data['text'] = text
    dict_data['like'] = like
    saveCommentJson("commentdata.json",dict_data)

