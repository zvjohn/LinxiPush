# Author: lindaye
# update: 2023-08-25 19:00
# http://mr1692750884645.aidhtjj.cn/coin/index.html?mid=CR42F6WUF 【元宝阅读】
# http://mr1692750916083.dsxanvq.cn/ox/index.html?mid=RG7UUSYFS 【星空阅读】
# http://mr1692750963995.stijhqm.cn/user/index.html?mid=D33C7W3A3 【花花阅读】
# 关注微信测试号(不关注无法推送检测文章): https://s1.ax1x.com/2023/08/23/pPJ5bnA.png
# 使用方法: 1.关注测试号 2.修改wxname的微信昵称 3.将cookie填写到data
# Version:V0.4

import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX3461 Build/RKQ1.210503.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/7925 MicroMessenger/8.0.40.2420(0x28002851) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
    'Cookie':'',
}
# 推送域名
tsurl = 'https://linxi-send.run.goorm.app'
# 临时用户名
temp_user = ''
# 微信昵称
wxname = "XX"
# Cookie填这
data = {"un":"##","token":"##","pageSize":20}


def test(link):
    result = requests.post(tsurl+"/task",json={"biz":temp_user,"url":link}).json()
    WxSend(f"微信阅读-{ydname}阅读", f"{temp_user}-检测文章", "请在30秒内完成当前文章",tsurl+"/read/"+temp_user)
    check = ''
    for i in range(30):
        result = requests.get(tsurl+"/back/"+temp_user).json()
        if result['status'] == True:
            check = True 
            break
        else:
            print("等待检测中...", end="\r", flush=True)
        time.sleep(1)
    if result['status'] == False:
        print("手动检测超时,验证失败!")
        check = False 
    return check

# 微信推送
def WxSend(project, status, content,turl):
    data = {
        "name": wxname, # 微信昵称
        "project": project,
        "status": status,
        "content": content,
        "url":turl
    }
    result = requests.post(tsurl, json=data).json()
    print(f"微信消息推送: {result['msg']}")
    if result['msg'] != "消息推送成功!":
        print(f"请手动完成验证吧: {tsurl}")


def user():
    url = domain +'/info'
    result = requests.post(url,headers=headers,json=data).json()['result']
    print(f"{ydname}账号: {result['uid']} 今日已读: {result['dayCount']} 今日积分:{result['moneyCurrent']}")
    global temp_user
    temp_user = result['uid']
    if ydname == "花花":
        options = [0.3, 0.5, 1, 5]  # 可选的数字列表
    else:
        options = [0.3, 1, 5, 10]  # 可选的数字列表
    max_money = max(filter(lambda x: x < (int(result['moneyCurrent'])/10000), options), default=0.3)
    return max_money

def read():
    while True:
        result = requests.post(domain +'/read',headers=headers,json=data).json()
        if result['code'] == 0:
            if result["result"]["status"] == 10:
                biz=''.join(re.findall('__biz=(.+)&mid',result["result"]["url"]))
                if biz in ['Mzg2Mzk3Mjk5NQ==']:
                    print("检测文章: 请在30秒内完成当前文章")
                    check = test(result["result"]["url"])
                    if check == True:
                        print("检测文章-过检测成功啦!")
                        result = requests.post(domain +'/submit',headers=headers,json=data).json()
                        print(result)
                    else:
                        print("检测文章-过检测失败啦!")
                        break
                else:
                    print(f"开始阅读文章-{biz}-阅读时间 6s")
                    time.sleep(6)
                    result = requests.post(domain +'/submit',headers=headers,json=data).json()["result"]
                    print(f"阅读成功: 积分{result['val']} 剩余{result['progress']}篇")  
            else:
                tips = {30:'重新运行尝试一下',40:'文章还没有准备好',50:'阅读失效,黑号了',60:'已经全部阅读完了',70:'下一轮还未开启',}
                print(f'{ydname}账号提醒: {tips[result["result"]["status"]]}!')
                if result["result"]["status"] ==30:
                    time.sleep(1)
                    continue
                else:
                    break
        else:
            if result['msg'] == "请求频繁":
                time.sleep(1)
                continue
            else:
                print(f"异常: {result}")
                break

def get_money(max_money):
    time.sleep(2)
    print(f"=================={ydname}提现====================")
    if ydname == "花花":
        t = "/wd"
    else:
        t = "/wdmoney"
    T_data = {"val":str(int(max_money*10000)),"un":data['un'],"token":data['token'],"pageSize":20}
    response = requests.post(domain+t, headers=headers, json=T_data).json()
    if response['code'] == 0:
        print(f"提现成功: {max_money}元")
    else:
        print(f"提现失败: {response['msg']}")

for i in ['/user','/coin','/ox']:
    domain = 'http://u.cocozx.cn/api'+i # 花花 /user 元宝阅读 /coin 星空阅读 /ox
    ydlist = {'/user':'花花','/coin':'元宝','/ox':'星空'}
    ydname = ydlist[i]
    print(f"=================={ydname}阅读====================")
    max_money = user()  # 提现金额
    read()
    max_money = user()  # 提现金额
    time.sleep(1)
    get_money(max_money)
    time.sleep(1)
