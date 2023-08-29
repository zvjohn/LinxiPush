# Author: lindaye
# update: 2023-08-29 13:00
# 更新: 1.添加wxpusher备用推送,替换林夕微信推送助手V1.0,无上限人数限制 2.林夕微信推送助手V1.0(关注人数达到上限,老用户不受影响) 
# wxpusher 使用教程: 扫码获取UID(填写到wxname): https://wxpusher.zjiecode.com/demo/
# 入口: http://tg.1693268703.api.mengmorwpt2.cn/h5_share/ads/tg?user_id=124922
# V0.1
import time
import requests
import random
import re
import urllib.parse

checkDict = {
    "MzkzNjI3NDAwOA==": ["木新领袋管家", "gh_04e096463e91"],
}

CKList = [
    {"name": "备注", "Authorization": "XXX"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
    'content-type': 'application/json',
    'Referer': 'http://71692693186.tt.bendishenghuochwl1.cn/',
}

ss = requests.session()
# 推送域名
tsurl = 'https://linxi-send.run.goorm.app'
# 临时用户名
temp_user = ""
# wxpusher的UID
wxname = ''

def user(name):
    result = ss.post('http://api.mengmorwpt1.cn/h5_share/user/info',headers=headers,json={"openid":0}).json()
    if result['code'] == 200:
        print(f'当前账号: {result["data"]["nickname"]} 当前积分: {result["data"]["points"]-result["data"]["used_points"]}')
    else:
        print(f"获取账号异常,请检查{name}的Authorization是否正确!")
        exit()


def sign_in():
    result = ss.post('http://api.mengmorwpt1.cn/h5_share/user/sign',headers=headers,json={"openid":0}).json()
    if result['code'] == 200:
        print(f"签到 - {result['message']}")
    else:
        print(f"获取账号异常")


def do_read():
    result = ss.post('http://api.mengmorwpt1.cn/h5_share/daily/get_read',headers=headers,json={"openid":0}).json()
    if result['code'] == 200:
        # 获取推荐阅读链接
        link = result['data']['link']
        print(f"获取阅读链接成功: 即将开始本轮阅读!")
        while True:
            result = ss.post('https://api.wanjd.cn/wxread/articles/tasks',headers=headers,json={'href':link}).json()
            if result['code'] == 200:
                data = [item for item in result['data'] if 'url' in item]
                if data != []:
                    data = data[0]                
                    s = random.randint(6,10)
                    biz = re.findall("biz=(.*?)&mid",data['url'])
                    if biz != []:
                        biz = biz[0]
                    else:
                        print(f"该文章没有biz:{data['url']}")
                        biz = re.findall("biz=(.*?)&amp;",ss.get(data['url']).text)[0]
                    print(f"获取阅读文章成功({biz}): 模拟阅读{s}秒")
                    if biz in checkDict:
                        check = test(biz,data['url'])
                        if check:
                            print("检测文章-过检测成功啦!")
                            time.sleep(s)
                            r_result = ss.post('https://api.wanjd.cn/wxread/articles/three_read',headers=headers,json={'id':data['id'], 'href': link}).json()
                            print(f"阅读结果: {r_result}")
                        else:
                            print("检测文章-过检测失败啦!")
                            break
                    else:
                        time.sleep(s)
                        r_result = ss.post('https://api.wanjd.cn/wxread/articles/three_read',headers=headers,json={'id': data['id'], 'href': link}).json()
                        print(f"阅读结果: {r_result}")
                else:
                    t_result = ss.post('https://api.wanjd.cn/wxread/articles/check_success', headers=headers, json={'type': 1, 'href': link}).json()
                    if t_result['code'] == 200:
                        print(f"恭喜! 本轮阅读已全部完成: {t_result['message']}")
                    else:
                        print(f"本轮阅读异常错误: {t_result}")
                        break
            else:
                print(f"获取阅读任务错误: {result}")
                break
    else:
        print(f"获取阅读链接失败: {result['message']}")


def get_money():
    result = ss.post('http://api.mengmorwpt1.cn/h5_share/user/withdraw', headers=headers, data={"openid":0}).json()
    if result['code'] == 200:
        print(f"提现结果: {result}")
    else:
        print(f"提现失败: {result['message']}")


def test(biz,link):
    result = ss.post(tsurl+"/task",json={"biz":temp_user+biz,"url":link}).json()
    WxSend("微信阅读-美添赚", f"检测文章", "请在60s内阅读当前文章",tsurl+"/read/"+temp_user+biz)
    check = ''
    for i in range(30):
        result = ss.get(tsurl+"/back/"+temp_user+biz).json()
        if result['status'] == True:
            check = True 
            break
        else:
            print("等待检测中...", end="\r", flush=True)
        time.sleep(2)
    if result['status'] == False:
        print("手动检测超时,验证失败!")
        check = False 
    return check


# 微信推送
def WxSend(project, status, content,turl):
    turl = urllib.parse.quote(turl)
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{wxname}?content={status}-{project}%0A{content}%0A%3Cbody+onload%3D%22window.location.href%3D%27{turl}%27%22%3E').json()
    print(f"微信消息推送: {result['msg']}")



for i in CKList:
    headers['Authorization'] = i['Authorization']
    temp_user =  i['Authorization']
    user(i['name'])
    sign_in()
    do_read()
    get_money()
    user(i['name'])
