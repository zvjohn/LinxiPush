# Author: lindaye
# Update:2023-09-20
# 新小阅阅读
# 活动入口：https://x.moonbox.site/?BAZZYYha7302#/?recommend=HU3PZX6MGU0
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量xxyytoken 值{"ck":"Cookie中app-token"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"ck":"Cookie中app-token"},{"ck":"Cookie中app-token"}]
# 软件版本
version = "0.0.1"
import requests
import json
import os
import time
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
Limit = 2
# 新小阅阅读域名(无法使用时请更换)
domain = 'https://x.moonbox.site/api'
# 保持连接,重复利用
ss = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309062f) XWEB/8379 Flue',
    'Content-Type': 'application/json'
}

def user_info(i,ck):
    headers['Cookie'] = f'app-token="{ck["ck"]}"'
    result = ss.get(domain+'/user/info',headers=headers).json()
    if result['data'] != None:
        print(f"账号【{i+1}】用户:{result['data']['nickname']} 余额:{result['data']['balance']}")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False


def do_read(i,ck):
    headers['Cookie'] = f'app-token="{ck["ck"]}"'
    while True:
        url = "https://x.moonbox.site/api/article/read"
        data = {"articleId": 344,"articleUser": 114,"bigTop": 0,"publishId": 349,"viewNum": "146","readType": 0,"channel": "0","readerDate": 1695174062000,"seconds": 34}
        result = ss.post(url, headers=headers, json=data).json()
        if result['code'] == 0:
            print(f"账号【{i+1}】{result['msg']}")
            break
        elif result['code'] == 1:
            if result['data'] != 0:
                print(f"账号【{i+1}】阅读文章成功-获得[{result['data']}]")
            else:
                print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
                return False


def get_money(i,ck):
    headers['Cookie'] = f'app-token="{ck["ck"]}"'
    result = ss.get(domain+'/user/info',headers=headers).json()
    if result['data'] != None:
        rmb = float(result['data']['balance'])
        result = ss.get(domain+"/account/withdraw/info", headers=headers).json()
        if result['code'] == 1:
            print(f"账号【{i+1}】余额:{rmb}豆 可提:{result['data']['canWithdrawDou']}豆  冻结:{result['data']['rateDou']}豆")
            if result['data']['canWithdrawDou'] >= (Limit*100):
                url = "https://x.moonbox.site/api/account/cash/withdraw"
                data = {"dou": result['data']['canWithdrawDou']}
                response = requests.post(url, headers=headers, json=data).json()
                if response['code'] == 1:
                    print(f"账号【{i+1}】提现成功-[{result['data']['canWithdrawDou']}]豆")
                else:
                    print(f"账号【{i+1}】提现失败-[{response}]")
            else:
                print(f"账号【{i+1}】未达到{Limit}元提现标准!")
        elif result['code'] == 405:
            print(f"{result['msg']}")
        else:
            print(f"错误未知{result}")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False





if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗██╗  ██╗██╗   ██╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚██╗██╔╝╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝  ╚███╔╝  ╚████╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗  ██╔██╗   ╚██╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗██╔╝ ██╗   ██║      ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═════╝ 
    项目:新小阅阅读                 BY-林夕               Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv('xxyytoken') == None:
            print('青龙变量异常: 请添加xxyytoken变量示例:{"ck":"xxxx"} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('xxyytoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"ck":"xxxx"}
        ]
        if ck_token == []:
            print('本地变量异常: 请添加本地ck_token示例:{"ck":"xxxx"}')
    # 创建进程池
    with Pool() as pool:
        # 并发执行函数
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))
        print("==================开始阅读文章=================")
        pool.starmap(do_read, list(enumerate(ck_token)))
        print("==================开始账号提现=================")
        pool.starmap(get_money, list(enumerate(ck_token)))


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[新小阅阅读V{version}]===============")
