# Author: lindaye
# Update:2023-09-26
# 值白说小程序
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量zbstoken 值{"ck":"X-Dts-Token的值"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"ck":"X-Dts-Token的值"},{"ck":"X-Dts-Token的值"}]
# 软件版本
version = "0.0.1"
name = "值白说"
linxi_token = "zbstoken"
linxi_tips = '{"ck":"X-Dts-Token的值"}'
import requests
import json
import os
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
# Limit = 0
# 值白说域名(无法使用时请更换)
domain = 'https://www.kozbs.com/demo/wx'
# 保持连接,重复利用
ss = requests.session()
headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39 (0x18002733) NetType/WIFI Language/zh_CN',
}

def user_info(i,ck):
    headers['X-Dts-Token'] = ck['ck']
    result = ss.get(domain+"/user/getUserIntegral",headers=headers).json()
    if result['errno'] == 0  and result['data']['list'] !=[]:
        print(f"账号【{i+1}】用户:{result['data']['list'][0]['userName']} 积分:{result['data']['integer']}")
    else:
        print(f"账号【{i+1}】获取用户信息失败!")


def do_task(i,ck):
    headers['X-Dts-Token'] = ck['ck']
    result = ss.get(domain+"/home/signDay",headers=headers).json()
    if result['errno'] == 0:
        print(f"账号【{i+1}】签到任务-每日: 签到成功[{result['data']['signCount']}]积分!")
    else:
        print(f"账号【{i+1}】签到任务-每日: 签到失败{result}")
    for j in range(3):
        result = requests.get(domain+"/user/addIntegralByShare", headers=headers).json()
        if result['errno'] == 0:
            print(f"账号【{i+1}】分享任务-第({j+1}): 分享成功!")
        else:
            print(f"账号【{i+1}】分享任务-第({j+1}): 分享失败{result}")




if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗███████╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚══███╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝   ███╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗  ███╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗███████╗   ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═════╝ 
    项目:{name}           BY-林夕          Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv(linxi_token) == None:
            print(f'青龙变量异常: 请添加{linxi_token}变量示例:{linxi_tips} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv(linxi_token).splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            # 这里填写本地变量
        ]
        if ck_token == []:
            print(f'本地变量异常: 请添加本地ck_token示例:{linxi_tips}')

    # 创建进程池
    with Pool() as pool:
        # 并发执行函数
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))
        print("==================开始执行任务=================")
        pool.starmap(do_task, list(enumerate(ck_token)))
        print("==================获取账号信息=================")
        pool.starmap(user_info, list(enumerate(ck_token)))


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
