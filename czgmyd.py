# Author: lindaye
# update: 2023-08-29 16:00
# 充值购买阅读(钢镚阅读)
# 入口: http://2496831.zpf7swrv.bnpgkgzod0b9.cloud/?p=2496831
# 使用方法: 1.填写cookie_list的值(可以全Cookie也可以"gfsessionid=xxxxx") 2.扫码关注Wxpusher 3.修改Wxpusher微信UID
# wxpusher 使用教程: 扫码获取UID(填写到wxname): https://wxpusher.zjiecode.com/demo/
# V1.1.6(正式版)

import re
import time
import hashlib
import random
import requests
import base64
import urllib.parse

# 抓包获取Cookie完全填入cookie替换###
cookie_list = ["##","##"]
# Wxpusher微信UID
wxname = 'XX'


# 推送域名
tsurl = 'https://linxi-send.run.goorm.app'
# 临时用户名
temp_user = ''
# 保持连接,重复利用
ss = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; V1923A Build/PQ3B.190801.06161913; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/5635 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
    "Cookie": "",
}


def get_sign():
    current_time = str(int(time.time()))
    # 计算 sign
    sign_str = f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
    sha256_hash = hashlib.sha256(sign_str.encode())
    sign = sha256_hash.hexdigest()
    data = f'time={current_time}&sign={sign}'
    return data

def home():
    url = "http://2477726.neavbkz.jweiyshi.r0ffky3twj.cloud/share"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    share_link = response["data"]["share_link"][0]
    p_value = share_link.split("=")[1].split("&")[0]
    global temp_user
    temp_user = p_value
    url = "http://2477726.neavbkz.jweiyshi.r0ffky3twj.cloud/read/info"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    if response["code"] == 0:
        remain = response["data"]["remain"]
        read = response["data"]["read"]
        print(f"ID:{p_value}   钢镚余额:{remain}\n今日阅读量:{read} 篇\n推广链接:{share_link}")
    else:
        print(response["message"])


def read():
    check_num = 0
    while True:
        url = "http://2496831.o5dukl6ba8wl.2yr7gmgnc2jat.cloud/read/task"
        response = ss.get(url, headers=headers, data=get_sign()).json()
        if response["code"] == 1:
            if "秒" in response['message']:
                print(response["message"])
                s = re.findall('请(.*?)秒',response['message'])[0]
                time.sleep(int(s))
            else:
                print(response["message"])
                break
        else:
            try:
                s = random.randint(10,15)
                # 检测是否是检测文章
                biz = re.findall("biz=(.*?)&",response["data"]["link"])[0]
                print(f"获取文章成功---{biz}---阅读时间{s}")
                if biz in check_list:
                    if check_num <= 1:
                        print(f"获取到检测文章,已推送到微信,请60s内完成验证!")
                        check_num += 1
                        # 过检测
                        check = test(biz,response["data"]["link"])
                        if check == True:
                            print("检测文章-过检测成功啦!")
                            time.sleep(s)
                            response = ss.post("http://2496831.o5dukl6ba8wl.2yr7gmgnc2jat.cloud/read/finish", headers=headers, data=get_sign()).json()  
                            print(f"阅读文章: {response}")
                        else:
                            print("检测文章-过检测失败啦!")
                            break
                    else:
                        print("获取到多次检测文章-已自动停止防止黑号,请手动去处理!")
                        break
                else:
                    time.sleep(s)
                    url = "http://2496831.o5dukl6ba8wl.2yr7gmgnc2jat.cloud/read/finish"
                    response = ss.post(url, headers=headers, data=get_sign()).json()
                    if response["code"] == 0:
                        if response["data"]["check"] is False:
                            gain = response["data"]["gain"]
                            print(f"阅读文章成功---获得钢镚[{gain}]")
                        else:
                            print(f"获取到未收录检测: {biz} 将自动停止脚本")
                            break
                    else:
                        if response['message'] == "记录无效":
                            print("记录无效,重新阅读")
                        else:
                            print(response)
                            break

            except KeyError:
                if response['code'] == 801:
                    print(f"今日任务已完成: {response['message']}")
                    break
                else:
                    print(f"获取文章失败,错误未知{response}")
                    break



def get_money():
    print("============开始微信提现============")
    url = "http://2496831.o5dukl6ba8wl.2yr7gmgnc2jat.cloud/withdraw/wechat"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    if response["code"] == 0:
        print(response["message"])
    elif response["code"] == 1:
        print(response["message"])
    else:
        print(f"错误未知{response}")


def test(biz,link):
    result = ss.post(tsurl+"/task",json={"biz":temp_user+biz,"url":link}).json()
    print(f"手动微信阅读链接: {link}")
    WxSend("微信阅读-钢镚阅读", "检测文章", "请在60s内阅读当前文章",tsurl+"/read/"+temp_user+biz)
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
    print(f"手动检测链接: {turl}")


for cookie in cookie_list:
    headers["Cookie"]=cookie
    home()
    read()
    get_money()
