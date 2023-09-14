# Author: lindaye
# V0.1
# 本地和青龙二选一
# 低保项目0.3/天
# 入口:http://redpage230617.read.biwuzhaojin.com/web-read/read?channelId=230327002
# 跳转到浏览器复制URL,提取里面的readUserid以及sign填入下面uid和sign即可
# 本地请在脚本最下方添加示例:{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}到本地变量ck_token

import requests
import json
import os
from multiprocessing import Pool

# 变量类型(二选一): 青龙、本地
Btype = "本地"

def read(index,ck):
    print(f"当前第{str(index+1)}个账号: 开始阅读")
    for i in range(30):
        # timestamp = int(time.time() * 1000)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309062f) XWEB/8379 Flue',
            'Referer': 'http://sc0909123703.wkyvch9n2.cn/',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
        }
        rurl = f'http://red1.read.biwuzhaojin.com/web-read/get-url?readUserId={ck["uid"]}'
        result = requests.get(rurl).json()
        if result['code']==200:
            pass
        else:
            print(f"当前第{str(index+1)}个账号: 阅读失败 {result['msg']}")
            break
        # url = f'http://gcold.youhujia.top/dxyuedu/?ch=3521&callbackUrl=http%3A%2F%2Fred1.read.biwuzhaojin.com%2Fweb-read%2Fget-url%3FreadUserId%3D{id["uid"]}&t={timestamp}&rbid=11111&cb=w&host=sc0909123703.wkyvch9n2.cn'
        # result = requests.get(url).text
        # print(result)
    print(f"当前第{str(index+1)}个账号: 阅读任务完成")
    uurl = 'http://redpage230617.read.biwuzhaojin.com/web-read/read-info'
    data = f'code=null&channelId=230327002&readUserId={ck["uid"]}&sign={ck["sign"]}'
    result = requests.post(uurl,data=data,headers=headers).json()
    print(f"当前第{str(index+1)}个账号: 钱包余额: {result['data']['walletMoney']}")
    turl = 'http://redpage230617.read.biwuzhaojin.com/web-read/cash-out'
    tdata = f'readUserId={ck["uid"]}&sign={ck["sign"]}'
    result = requests.post(turl,data=tdata,headers=headers).json()
    if result['code'] == 200:
        print(f"当前第{str(index+1)}个账号: 提现成功 {result['data']['topTitle']}")
    else:
        print(f"当前第{str(index+1)}个账号: 提现失败 {result['msg']}")

if __name__ == '__main__':
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗       ██████╗    ██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔═████╗   ╚════██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║██╔██║    █████╔╝
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝████╔╝██║    ╚═══██╗
███████╗██║██║ ╚████║██╔╝ ██╗██║      ╚██████╔╝██╗██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝       ╚═════╝ ╚═╝╚═════╝ 
    项目:低保0.3       BY-林夕       Verion: 0.1(并发)
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
             
        ]
        if ck_token == []:
            print('账号异常: 请添加本地ck_token示例:{"uid":"123456","sign":"92avddsvs545sdvsd1v515s1dv"}')
    with Pool() as pool:
        # 使用enumerate函数获取每个ID在列表中的索引，并与ID值一起作为参数传递给test函数
        # 使用map方法将每个元组作为参数提交到进程池中
        pool.starmap(read, list(enumerate(ck_token)))
