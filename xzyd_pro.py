# Author: lindaye
# Update:2023-09-26
# 小啄阅读
# 建议一天执行两次(或许有意外之喜)
# 活动入口：TG内部群
# 微信打开活动入口跳转到浏览器复制URL,提取里面的readUserid以及sign填入下面uid和sign即可
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量xztoken 值{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"},{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}]
# 软件版本
version = "0.0.3"
name = "小啄阅读"
linxi_token = "xztoken"
linxi_tips = '{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}'
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
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
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
    for i in range(30):
        rurl = f'http://red1.read.biwuzhaojin.com/web-read/get-url?readUserId={ck["uid"]}'
        result = ss.get(rurl).json()
        if result['code']==200:
            check = True
        else:
            check = False
            print(f"账号【{i+1}】阅读失败:{result['msg']}")
            break
    if check:
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
        print(f"================[{name}V{version}]===============")
