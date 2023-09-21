# Author: lindaye
# Update:2023-09-20
# 小啄阅读
# 建议一天执行两次(或许有意外之喜)
# 活动入口：TG内部群
# 微信打开活动入口跳转到浏览器复制URL,提取里面的readUserid以及sign填入下面uid和sign即可
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量xztoken 值{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"},{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}]
# 软件版本
version = "0.0.2"
import requests
import json
import os
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
# Limit = 0
# 小啄阅读域名(无法使用时请更换)
domain = 'http://redpage230617.read.biwuzhaojin.com'
# 保持连接,重复利用
ss = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309062f) XWEB/8379 Flue',
    'Referer': 'http://sc0909123703.wkyvch9n2.cn/',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}

def user_info(i,ck):
    data = f'code=null&channelId=230327002&readUserId={ck["uid"]}&sign={ck["sign"]}'
    result = ss.post(domain+'/web-read/read-info',data=data,headers=headers).json()
    if result['code'] == 201:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False
    else:
        print(f"账号【{i+1}】钱包余额: {result['data']['walletMoney']}")


def do_read(i,ck):
    print(f"账号【{i+1}】开始阅读")
    for i in range(30):
        rurl = f'http://red1.read.biwuzhaojin.com/web-read/get-url?readUserId={ck["uid"]}'
        result = ss.get(rurl).json()
        if result['code']==200:
            pass
        else:
            print(f"账号【{i+1}】阅读失败:{result['msg']}")
            break
    print(f"账号【{i+1}】阅读任务完成")


def get_money(i,ck):
    tdata = f'readUserId={ck["uid"]}&sign={ck["sign"]}'
    result = ss.post(domain+'/web-read/cash-out',data=tdata,headers=headers).json()
    if result['code'] == 200:
        print(f"账号【{i+1}】提现成功 {result['data']['topTitle']}")
    else:
        print(f"账号【{i+1}】提现失败 {result['msg']}")




if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗███████╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚══███╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝   ███╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗  ███╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗███████╗   ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═════╝ 
    项目:小啄阅读(几秒到低保0.3)       BY-林夕       Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv('xztoken') == None:
            print('账号Cookie异常: 请添加xztoken变量示例:{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('xztoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"uid":"xxxx","sign":"xxxx"}
        ]
        if ck_token == []:
            print('账号异常: 请添加本地ck_token示例:{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}')

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
        print(f"================[小啄阅读V{version}]===============")
