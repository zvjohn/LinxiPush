# Author: lindaye
# V1.1.6
# 活动入口：http://2496831.sl4mwis5.gbl.avc14qvjzax7.cloud/?p=2496831
# 变量gbtoken 值{"ck":"ysm_uid的值","ts":"Wxpusher的UID"} 一行一个
import requests
from multiprocessing import Pool
import re
import time
import hashlib
import random
import os
import json
from urllib.parse import unquote,quote


# 检测列表
check_list = [
    'MzkyMzI5NjgxMA==','MzkzMzI5NjQ3MA==','Mzg5NTU4MzEyNQ==', 'Mzg3NzY5Nzg0NQ==', 'MzU5OTgxNjg1Mg==',
    'Mzg4OTY5Njg4Mw==', 'MzI1ODcwNTgzNA=='
]

def get_sign():
    current_time = str(int(time.time()))
    # 计算 sign
    sign_str = f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
    sha256_hash = hashlib.sha256(sign_str.encode())
    sign = sha256_hash.hexdigest()
    data = f'time={current_time}&sign={sign}'
    return data


def test(index,ck):
    # 保持连接,重复利用
    ss = requests.session()
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; V1923A Build/PQ3B.190801.06161913; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/5635 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
        "Cookie":f"gfsessionid={ck['ck']};"
    }
    url = "http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/share"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    share_link = response["data"]["share_link"][0]
    p_value = share_link.split("=")[1].split("&")[0]
    global temp_user
    temp_user = p_value
    url = "http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/read/info"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    if response["code"] == 0:
        remain = response["data"]["remain"]
        read = response["data"]["read"]
        print(f"当前账号【{str(index+1)}】: ID:{p_value}   钢镚余额:{remain}  今日阅读量:{read} 篇  推广链接:{share_link}")
    else:
        print(response["message"])
    while True:
        url = "http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/read/task"
        response = ss.get(url, headers=headers, data=get_sign()).json()
        if response["code"] == 1:
            if "秒" in response['message']:
                print(f"当前账号【{str(index+1)}】即将开始阅读:{response['message']}")
                time.sleep(5)
            else:
                print(f"当前账号【{str(index+1)}】{response['message']}")
                break
        else:
            try:
                s = random.randint(10,12)
                # 检测是否是检测文章
                biz = re.findall("biz=(.*?)&",response["data"]["link"])[0]
                print(f"当前账号【{str(index+1)}】获取文章成功---{biz}---阅读时间{s}")
                if biz in check_list:
                    print(f"当前账号【{str(index+1)}】获取到检测文章,已推送到微信,请60s内完成验证!")
                    # 过检测
                    check = check_status(ck['ts'],response["data"]["link"])
                    if check == True:
                        print("当前账号【{str(index+1)}】检测文章-过检测成功啦!")
                        response = ss.post("http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/read/finish", headers=headers, data=get_sign()).json()
                        print(f'当前账号【{str(index+1)}】阅读文章成功---获得钢镚[{response["data"]["gain"]}]---已读{response["data"]["read"]}篇')
                    else:
                        print(f"当前账号【{str(index+1)}】检测文章-过检测失败啦!")
                        break
                else:
                    time.sleep(s)
                    url = "http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/read/finish"
                    response = ss.post(url, headers=headers, data=get_sign()).json()
                    # print(response)
                    if response["code"] == 0:
                        if response["data"]["check"] is False:
                            print(f'当前账号【{str(index+1)}】阅读文章成功---获得钢镚[{response["data"]["gain"]}]---已读{response["data"]["read"]}篇')
                        else:
                            print(f"当前账号【{str(index+1)}】获取到未收录检测: {biz} 将自动停止脚本")
                            break
                    else:
                        if response['message'] == "记录无效":
                            print(f"当前账号【{str(index+1)}】记录无效,重新阅读")
                        else:
                            print(f"当前账号【{str(index+1)}】{response}")
                            break
            except KeyError:
                if response['code'] == 801:
                    print(f"当前账号【{str(index+1)}】今日任务已完成: {response['message']}")
                    break
                else:
                    print(f"当前账号【{str(index+1)}】获取文章失败,错误未知{response}")
                    break
    url = "http://2496831.marskkqh7ij0j.jpsl.u1jcnc75wwbyk.cloud/withdraw/wechat"
    response = ss.get(url, headers=headers, data=get_sign()).json()
    if response["code"] == 0:
        print(f'当前账号【{str(index+1)}】开始提现:{response["message"]}')
    elif response["code"] == 1:
        print(f'当前账号【{str(index+1)}】开始提现:{response["message"]}')
    else:
        print(f'当前账号【{str(index+1)}】未知错误:{response}')


def check_status(key,link):
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-钢镚阅读%0A请在60秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
    print(f"微信消息推送: {result['msg']}")
    print(f"手动微信阅读链接: {link}")
    time.sleep(30)
    return True


if __name__ == '__main__':
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗       ██████╗ ██████╗ ██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔════╝ ██╔══██╗╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║  ███╗██████╔╝ ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██║   ██║██╔══██╗  ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║      ╚██████╔╝██████╔╝   ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝       ╚═════╝ ╚═════╝    ╚═╝   ╚═════╝ 
                    BY-林夕               Verion: 1.1.7(并发)
""")

    if os.getenv('gbtoken') == None:
        print("账号Cookie异常: 请添加gbtoken变量!")
        exit()
    # CK列表
    ck_token = [json.loads(line) for line in os.getenv('gbtoken').splitlines()]
    # 创建进程池，默认会根据系统的CPU核心数创建相应数量的进程
    with Pool() as pool:
        # 使用enumerate函数获取每个ID在列表中的索引，并与ID值一起作为参数传递给test函数
        # 使用map方法将每个元组作为参数提交到进程池中
        pool.starmap(test, list(enumerate(ck_token)))
