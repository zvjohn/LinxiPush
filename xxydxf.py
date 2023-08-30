# Author: lindaye
# V1.1.6
# 2023.8.30更新:
#   1.改为变量ck,一行一个ck示例
#   2.采用Wxpusher进行推送服务(手动过检测),仅需扫码获取UID,无需其他操作
# Wxpusher获取UID: https://wxpusher.zjiecode.com/demo/
# 变量名 xyytoken 示例: {"ck":"这里是cookie中ysm_uid的值","ts":"这里是Wxpusher获取UID"}

import requests
import re
import time
import random
import os
from urllib.parse import unquote,quote

ck_token = [eval(line) for line in os.getenv('xyytoken').strip().split('\n')]

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380'
}

check_list = [
    "MzkxNTE3MzQ4MQ==",
    "Mzg5MjM0MDEwNw==",
    "MzUzODY4NzE2OQ==",
    "MzkyMjE3MzYxMg==",
    "MzkxNjMwNDIzOA==",
    "Mzg3NzUxMjc5Mg==",
    "Mzg4NTcwODE1NA==",
    "Mzk0ODIxODE4OQ==",
    "Mzg2NjUyMjI1NA==",
    "MzIzMDczODg4Mw==",
    "Mzg5ODUyMzYzMQ==",
    "MzU0NzI5Mjc4OQ==",
    "Mzg5MDgxODAzMg==",
]


# 保持连接,重复利用
ss = requests.session()
# 推送域名
tsurl = 'https://linxi-send.run.goorm.app'
# 临时ck
ysm_uid= ''
# 微信昵称
WxpusherUid = ''

def ts ():
    return str (int (time .time ()))+'000'


def signin():
    result = ss.get('http://1692416143.3z2rpa.top/',headers=headers).text
    signid = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if signid == []:
        print ('初始化失败,账号异常')
        exit()
    else:
        print ('初始化成功,账号登陆成功!')
        return signid


def get_money(signid):
    result = ss.get(f'http://1692429080.3z2rpa.top/yunonline/v1/exchange?unionid={ysm_uid}&request_id={signid}&qrcode_number=&addtime=').text
    money = re.findall(r'id="exchange_gold">(.*?)</p>',result)
    if money == []:
        print ('金币获取失败,账号异常')
    else:
        if int(money[0]) >= 3000:
            money = (int(money[0]) // 3000) * 3000
            print(f"提交体现金币: {money}")
            t_data = {'unionid':ysm_uid,'request_id':signid,'gold':money}
            t_result = ss.post('http://1692429080.3z2rpa.top/yunonline/v1/user_gold',json=t_data).json()
            if t_result['errcode'] == 0:
                print(f"金币转金额成功: {t_result['data']['money']}")
            else:
                print(f"金币转金额失败: {t_result['msg']}")
            j_data = {'unionid':ysm_uid,'signid':signid,'ua':0,'ptype':0,'paccount':'','pname':''}
            j_result = ss.post('http://1692422733.3z2rpa.top/yunonline/v1/withdraw',data=j_data).json()
            print(f"体现结果: {j_result['msg']}")
        else:
            print(f'还未到达提现最低金币 当前金币: {money[0]}')



def user_info():
    result = ss.get(f'http://1692416143.3z2rpa.top/yunonline/v1/sign_info?time={ts()}000&unionid={ysm_uid}').json()
    if result['errcode'] == 0:
        pass
    else:
        print ('获取用户信息失败，账号异常')

def hasWechat():
    result = ss.get(f'http://1692416143.3z2rpa.top/yunonline/v1/hasWechat?unionid={ysm_uid}').json()
    if result['errcode'] == 0:
        pass
    else:
        print ('获取用户信息失败，账号异常')

def gold():
    result = ss.get(f'http://1692416143.3z2rpa.top/yunonline/v1/gold?unionid={ysm_uid}&time={ts()}000').json()
    if result['errcode'] == 0:
        print(f"今日积分: {result['data']['day_gold']} 已阅读: {result['data']['day_read']}篇 剩余: {result['data']['remain_read']}篇")
    else:
        print ('获取用户信息失败，账号异常')


def get_Key():
    data = {'unionid':ysm_uid}
    result = ss.post('http://1692416143.3z2rpa.top/yunonline/v1/wtmpdomain',json=data).json()
    uk = re.findall(r'uk=([^&]+)',result['data']['domain'])
    print(f"获取到KEY: {uk[0]}")
    do_read(uk[0])

def do_read(uk):
    check_num = 0
    while True:
        result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}').json()
        if result['errcode'] == 0:
            link = result['data']['link']
            l_result = ss.get(link,headers=headers).text
            # 获取biz
            biz = re.findall("biz=(.*?)&amp;",l_result)[0]
            s = random.randint(6,8)
            print (f'获取文章成功-{biz}-本次模拟读{s}秒')
            if check_num <= 1:
                if biz in check_list:
                    print("阅读文章检测-已推送至微信,请60s内完成验证!")
                    check_num += 1
                    print(f"获取到微信文章: {link}")
                    # 过检测
                    check = test(biz,link)
                    if check == True:
                        print("检测文章-过检测成功啦!")
                        time.sleep(s)
                        r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                        if r_result['errcode'] == 0:
                            print(f"阅读已完成: 获得{r_result['data']['gold']}积分")
                        else:
                            print(r_result)
                            break
                    else:
                        print("检测文章-过检测失败啦!")
                        break
                else:
                    time.sleep(s)
                    r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                    if r_result['errcode'] == 0:
                        print(f"阅读已完成: 获得{r_result['data']['gold']}积分")
                    else:
                        print(f"阅读失败,获取到未收录检测BIZ:{biz}")
                        print(r_result)
                        break
            else:
                print("获取到多次检测文章-已自动停止防止黑号,请手动去处理!")
                break
        else:
            if result['msg'] == "任务重复" or result['msg'] == "任务超时":
                print(f"阅读失败: {result['msg']}重新获取文章")
            else:
                print (f"阅读提醒: {result['msg']}")
                break


def test(link):
    result = ss.post(tsurl+"/task",json={"biz":"xyy"+ysm_uid,"url":link}).json()
    WxSend("微信阅读-小阅阅读", f"{ysm_uid}-检测文章", "请在60s内阅读当前文章",tsurl+"/read/"+"xyy"+ysm_uid)
    check = ''
    for i in range(30):
        result = ss.get(tsurl+"/back/"+"xyy"+ysm_uid).json()
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
    turl = quote(turl)
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{WxpusherUid}?content={status}-{project}%0A{content}%0A%3Cbody+onload%3D%22window.location.href%3D%27{turl}%27%22%3E').json()
    print(f"微信消息推送: {result['msg']}")
    print(f"手动检测链接: {unquote(turl)}")


for i in ck_token:
    print(f"============当前第{ck_token.index(i)+1}个账户============")
    headers['Cookie'] = f"ysm_uid={i['ck']}"
    ysm_uid = i['ck']
    WxpusherUid = i['ts']
    signid = signin()
    user_info()
    hasWechat()
    gold()
    get_Key()
    gold()
    get_money(signid)
