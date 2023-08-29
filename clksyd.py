# Author: linxi
# update: 2023-08-29 7:00
# 从零开始阅读
# 入口: https://entry-1318684421.cos.ap-nanjing.myqcloud.com/cos_b.html?openId=oiDdr5xiVUIwNQVvj1sADz2rb5Mg
# 微信测试号: https://s1.ax1x.com/2023/08/23/pPJ5bnA.png
# 1.关注测试号 2.修改wxname微信昵称 3.替换authtoken为抓包的authtoken
# 更新: 1.添加wxpusher备用推送,替换林夕微信推送助手V1.0,无上限人数限制 2.林夕微信推送助手V1.0(关注人数达到上限,老用户不受影响) 
# wxpusher 使用教程: 扫码获取UID(填写到wxname): https://wxpusher.zjiecode.com/demo/
# V0.1.1(测试版)


import requests
from Crypto.Cipher import AES
import base64
import random
import re
import time

# 推送域名
tsurl = 'https://linxi-send.run.goorm.app'
# 临时用户名
temp_user = ''
# 微信昵称
wxname = 'XX'
# 保持连接,重复利用
ss = requests.session()
# 抓包获取Cookie中的authtoken替换###
authtoken = '###'

headers = {
    'Cookie': f'authtoken={authtoken}; snapshot=0',
    'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380'
}

def aes_encrypt(data):
    block_size = AES.block_size  # 获取AES块大小
    padding = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)  # 填充函数，使得数据长度为块大小的整数倍
    key = b'5e4332761103722eb20bb1ad53907c6e'  # 密钥，需要根据实际情况修改
    cipher = AES.new(key, AES.MODE_ECB)  # 使用ECB模式创建AES对象
    encrypted_data = cipher.encrypt(padding(data).encode())  # 对数据进行加密
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode()  # 对加密后的数据进行base64编码
    return encrypted_data_base64

def get_readhome():
    url = 'https://sss.mvvv.fun/app/enter/read_home'
    result = ss.get(url,headers=headers).json()
    if result['code'] == 0:
        url = "http://" + re.findall('//(.*?)/',result['data']['location'])[0]
        get_read(url)
    else:
        print("获取阅读域名失败!")
        get_read("http://hmqulo7g9p.qqaas.fun")


def get_read(url):
    result = ss.get(url+"/app/user/myPickInfo",headers=headers).json()
    if result['code'] == 401:
        print(f"账号异常:{result['msg']}")
    else:
        data = aes_encrypt(f'{{"moneyPick":{result["data"]["goldNow"]}}}')
        result = ss.post(url+"/app/user/pickAuto",headers=headers,json=data).json()
        print(f"兑换结果: {result['msg']}")
        result = ss.get(url+"/app/user/myInfo",headers=headers).json()['data']
        print(f"用户: {result['nameNick']} 今日已读: {result['completeTodayCount']}篇  获得积分: {result['completeTodayGold']}")
        global temp_user
        temp_user = result['nameNick']
        if result['remainSec'] == 0:
            print ('当前是读文章的状态')#line:93
            get_myinfo(url)
        else :#line:94
            ttime =int (result['remainSec'] /60 )#line:95
            print ('当前不是是读文章的状态,距离下次阅读还有',ttime ,'分钟')#line:96
    
    
def get_myinfo(url):
    result = ss.get(url+"/app/read/get",headers=headers).json()['data']['location']
    u = re.findall(r'u=([^&]+)',result)[0]
    print(f"获取到KEY: {u}")
    do_read(u)


def do_read(u):
    result = ss.get(f'https://sss.mvvv.fun/app/task/doRead?u={u}&type=1',headers=headers).json()['data']
    if result['bizCode'] !=0:
        tips = {20:'文章正在补充中，稍后再试',30:'下批文章将在24小时后到来',10:'下批文章将在60分钟后到达',11:'当天达到上限'}
        print(tips[result['bizCode']])
    else:
        taskKey = result['taskKey']
        print(f"阅读任务ID: {taskKey}")
        s = random.randint (10 ,12 )
        print(f"随机阅读 {s} 秒")
        time.sleep(s)
        read_check = False
        while True:
            if read_check == False:
                url = f'https://sss.mvvv.fun/app/task/doRead?u={u}&type=1&key={taskKey}'
                result = ss.get(url,headers=headers).json()['data']
                print(result)
                if result['bizCode'] == 0:
                    read_check = False
                    print(f"阅读结果: {result['detail']}")
                    taskKey = result['taskKey']
                    print(f"阅读任务ID: {taskKey}")
                    s = random.randint (10 ,12 )
                    print(f"随机阅读 {s} 秒")
                    time.sleep(s)
                elif (result['bizCode'] == 31) and (result['detail'] == "检测中"):
                    read_check = True
                    print(f"获取到检测文章,已推送到微信 60s")
                else:
                    print(f"任务刷爆了: {result}")
                    break
            else:
                # 过检测
                result = ss.get(f'https://sss.mvvv.fun/app/task/doRead?u={u}&type=1',headers=headers).json()['data']
                check = test(result['taskUrl'])
                if check == True:
                    print("检测文章-过检测成功啦!")
                    taskKey = result['taskKey']
                    print(f"阅读任务ID: {taskKey}")
                    s = random.randint (9 ,10 )
                    print(f"随机阅读 {s} 秒")
                    time.sleep(s)
                else:
                    print("检测文章-过检测失败啦!")
                    break


def test(link):
    result = ss.post(tsurl+"/task",json={"biz":temp_user,"url":link}).json()
    WxSend("微信阅读-微信阅读",f"{temp_user}-检测文章", "请在60秒内完成当前文章",tsurl+"/read/"+temp_user)
    check = ''
    for i in range(30):
        result = ss.get(tsurl+"/back/"+temp_user).json()
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

# 微信推送(备用)
def WxSend(project, status, content,turl):
    turl = urllib.parse.quote(turl)
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{wxname}?content={status}-{project}%0A{content}%0A%3Cbody+onload%3D%22window.location.href%3D%27{turl}%27%22%3E').json()
    print(f"微信消息推送: {result['msg']}")

get_readhome()
