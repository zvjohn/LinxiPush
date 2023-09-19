# 泉站桶装水小程序
# author:lindaye
# 变量示例:{"name":"真实姓名","token":"BVUVVUY"} 一行一个
# 低保项目(0.2)
version = "0.0.2"
import requests
import json
import os
import time
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
# Limit = 0
# 小啄阅读域名(无法使用时请更换)
domain = 'https://admin.dtds888.com/api/index'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8379',
    'Content-Type': 'application/json',
}

def user_info(i,ck):
    data = {"deviceType":"wxapp","timestamp":int(time.time()),"token":ck['token']}
    result = requests.post(domain + "/index/user_info",headers=headers,json=data).json()
    if result['msg'] == "success":
        print(f"账号【{i+1}】 用户: {result['data']['user']['user_nickname']} 余额: {result['data']['user']['balance']}")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")

def do_sign(i,ck):
    data = {"deviceType":"wxapp","timestamp":int(time.time()),"token":ck['token']}
    result = requests.post(domain + "/user/SignIn",headers=headers,json=data).json()
    print(f"账号【{i+1}】 签到: {result['msg']} {result['data']}")


def get_money(i,ck):
    data = {"deviceType":"wxapp","timestamp":int(time.time()),"token":ck['token']}
    rmb = requests.post(domain + "/index/user_info",headers=headers,json=data).json()['data']['user']['balance']
    if rmb >= 1.0:
        data['money'] = "1"
        data['name'] = ck['name']
        result = requests.post(domain+"/user/cashPost",headers=headers,json=data).json()
        print(f"账号【{i+1}】{result['msg']}")
    else:
        print(f"账号【{i+1}】 账号余额未达到1元提现标准!")




if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗       ██████╗ ███████╗████████╗███████╗███████╗
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔═══██╗╚══███╔╝╚══██╔══╝╚══███╔╝██╔════╝
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║   ██║  ███╔╝    ██║     ███╔╝ ███████╗
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██║▄▄ ██║ ███╔╝     ██║    ███╔╝  ╚════██║
███████╗██║██║ ╚████║██╔╝ ██╗██║      ╚██████╔╝███████╗   ██║   ███████╗███████║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝       ╚══▀▀═╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝
    项目:泉站桶装水(每日0.2)       BY-林夕       Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv('qztoken') == None:
            print('账号Cookie异常: 请添加qztoken变量示例:{"name":"张三","token":"BVUVVUY"}')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('qztoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"name":"xxx","token":"xxxx=="},
            {"name":"xxx","token":"xxxx=="}
        ]
        if ck_token == []:
            print('账号异常: 请添加本地ck_token示例:{"name":"张三","token":"BVUVVUY"}')

    # 创建进程池
    with Pool() as pool:
        # 并发执行函数
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))
        print("==================开始阅读文章=================")
        pool.starmap(do_sign, list(enumerate(ck_token)))
        print("==================开始账号提现=================")
        pool.starmap(get_money, list(enumerate(ck_token)))


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 输出结果
        print(f"================[泉站桶装水V{version}]===============")
