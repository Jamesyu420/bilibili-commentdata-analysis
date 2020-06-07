from json.decoder import JSONDecodeError
from requests import get

def decode_json(r):
    try:
        response = r.json()
    except JSONDecodeError:
        # 虽然用的是requests的json方法，但要捕获的这个异常来自json模块
        return False
    else:
        return response

def check(scan):
    k = scan[0:2]
    print(k)
    if k=="BV" or k=="bv":
        return bv2av(scan)
    elif k=="AV" or k=="av":
        return scan
    else:
        pass

def bv2av(bv):
    BV2AV_API = 'https://api.bilibili.com/x/web-interface/view'  # ?bvid=
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/80.0.3987.149 Safari/537.36'}
    r = get(BV2AV_API, {'bvid': bv}, headers=HEADER)
    response = decode_json(r)
    try:
        return str(response['data']['aid'])
    except (KeyError, TypeError):
        return False

s = "av71771532"
print(check(s))
