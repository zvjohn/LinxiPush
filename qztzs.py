import requests
import time
import os
import json
from multiprocessing import Pool

# 变量类型(二选一): 青龙、本地
Btype = "本地"

def qztzs(index,ck):
    ss = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8379',
        'Content-Type': 'application/json',

    }
    url = 'https://admin.dtds888.com/api/index/index/user_info'
    data = {"deviceType":"wxapp","timestamp":int(time.time()),"token":ck['token']}
    result = ss.post(url,headers=headers,json=data).json()
    if result['msg'] == "success":
        print(f"当前第[{index+1}]个账号 用户: {result['data']['user']['user_nickname']} 余额: {result['data']['user']['balance']}")
        rmb = result['data']['user']['balance']
        qurl = 'https://admin.dtds888.com/api/index/user/SignIn'
        result = ss.post(qurl,headers=headers,json=data).json()
        print(f"当前第[{index+1}]个账号 签到: {result['msg']} {result['data']}")
        if rmb >= 1.0:
            turl = 'https://admin.dtds888.com/api/index/user/cashPost'
            data['money'] = "1"
            data['name'] = ck['name']
            result = ss.post(turl,headers=headers,json=data).json()
            print(f"当前第[{index+1}]个账号 {result}")
        else:
            print(f"当前第[{index+1}]个账号 账号余额未达到提现标准!")
    else:
        print(f"当前第[{index+1}]个账号账号 登陆失败: 请检查Token!")

if __name__ == '__main__':
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗       ██████╗    ██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔═████╗   ╚════██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║██╔██║    █████╔╝
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝████╔╝██║    ╚═══██╗
███████╗██║██║ ╚████║██╔╝ ██╗██║      ╚██████╔╝██╗██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝       ╚═════╝ ╚═╝╚═════╝ 
    项目:泉站桶装水       BY-林夕       Verion: 0.1(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv('qztoken') == None:
            print('账号Cookie异常: 请添加qztoken变量示例:{"name":"xx","token":"Bscdsdsvsfdvfdv==="}')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('qztoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"name":"xx","token":"B==="},
        ]
        if ck_token == []:
            print('账号异常: 请添加本地ck_token示例:{"name":"xx","token":"Bscdsdsvsfdvfdv==="}')
    with Pool() as pool:
        # 使用enumerate函数获取每个ID在列表中的索引，并与ID值一起作为参数传递给test函数
        # 使用map方法将每个元组作为参数提交到进程池中
        pool.starmap(qztzs, list(enumerate(ck_token)))
