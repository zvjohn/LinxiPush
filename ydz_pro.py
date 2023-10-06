# Author: lindaye
# Update:2023-09-26
# 阅读赚
# 活动入口：http://5851226094.ppbelpz.cn/?jgwq=3340404&goid=itrb
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量ydztoken 值{"ck":"a_h_n最后一个/的后面的值或者ck里面的=后的值","ts":"Wxpusher的UID"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"ck":"a_h_n最后一个/的后面的值或者ck里面的=后的值","ts":"Wxpusher的UID"},{"ck":"a_h_n最后一个/的后面的值或者ck里面的=后的值","ts":"Wxpusher的UID"}]
# 脚本使用说明:
#   1.(必须操作)扫码关注wxpusher获取UID: https://wxpusher.zjiecode.com/demo/
#   2.在1打开的网页中点击发送文本消息,查看是否收到,收到可继续
#   3.将1打开的网页中的UID或者以及操作过1的账号UID复制备用
#   4.根据提示说明填写账号变量
# 回调服务器开放说明:
#   1.仅针对授权用户开放,需配合授权软件使用
#   2.青龙变量设置LID变量名,值为授权软件的LID
# 软件版本
version = "0.0.3"
name = "阅读赚"
linxi_token = "ydztoken"
linxi_tips = '{"ck":"a_h_n最后一个/的后面的值或者ck里面的=后的值","ts":"Wxpusher的UID"}'
import requests
import json
import time
import random
import re
import os
from multiprocessing import Pool
from urllib.parse import quote,unquote

# 阅读等待时间
tsleep = 40
# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
Limit = 2
# 授权设备ID(软件版本>=1.3.3)[非授权用户不填即可]
imei = os.getenv('LID')
# 阅读赚域名(无法使用时请更换)
domain = "http://wxr.jjyii.com"
# 保持连接,重复利用
ss = requests.session()
# 检测文章列表(如有未收录可自行添加)
check_list = [
    # 自行添加,TG内部群公布汇总
]

# 获取个人信息模块
def user_info(i,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
        'a_h_n': f'http%3A%2F%2F5851577307.gbvbmxo.cn%2F%3Fgoid%3Ditrb/{ck["ck"]}' 
    }
    result = requests.post(domain+"/user/getinfo?v=3",headers=headers).json()
    if 'code' not in result:
        print(f"账号【{i+1}】用户:{result['data']['id']} 当前金币:{result['data']['balance']} 已读:{result['data']['count']}篇")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False

# 阅读文章模块
def do_read(i,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
        'a_h_n': f'http%3A%2F%2F5851577307.gbvbmxo.cn%2F%3Fgoid%3Ditrb/{ck["ck"]}' 
    }
    result = requests.post(domain+"/user/getinfo?v=3",headers=headers).json()
    if 'code' not in result:
        count = result['data']['count']
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False
    headers = {
        "Content-Length": "82",
        "a_h_n": f"http%3A%2F%2F5851750682.qekzkqt.cn%2F%3Fa%3Dgt%26goid%3Ditrb%26_v%3D3890/{ck['ck']}",
        # 这里的UA
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://5851750682.qekzkqt.cn",
        "Referer": "http://5851750682.qekzkqt.cn/",
    }
    while True:
        data = f"o={quote(headers['Origin'])}%2F%3Fa%3Dgt%26goid%3Ditrb%26_v%3D3890&t=quick"
        result = requests.post(domain+"/r/get?v=10",headers=headers,data=data).json()
        if result['code'] == 2023:
            print(f"账号【{i+1}】获取文章失败:当前为二维码页面!")
        if result['data']['url'] == None:
            if result['data']['uiv'] == 1:
                print(f"账号【{i+1}】获取文章失败: 已黑号,请明天重试!")
                break
            else:
                if result['data']['hs'] > 0:
                    print(f"账号【{i+1}】获取文章失败: 下一轮文章到来{result['data']['hm']}分钟倒计时!")
                    break
                else:
                    print(f"账号【{i+1}】获取文章失败: 阅读更新中,尝试10秒后开始重试!")
                    time.sleep(10)           
        else:
            s = random.randint(11,12)
            biz = re.findall("biz=(.*?)&mid",result['data']['url'])
            if biz == []:
                biz =  re.findall("biz=(.*?)&amp;",requests.get(result['data']['url'],headers=headers).text)
                if biz == []:
                    print(f"未找到biz:{result['data']['url']}")
                    break
                else:
                    biz = biz[0]
            else:
                biz = biz[0]
            print(f"账号【{i+1}】获取文章成功-{biz}-模拟阅读{s}秒")
            if count in [2, 32, 62, 92] or biz in check_list:
                if biz in check_list:
                    print(f"账号【{i+1}】检测到已收录BIZ[{biz}]")
                else:
                    print(f"账号【{i+1}】检测到未收录BIZ[{biz}]请自动添加")
                print(f"账号【{i+1}】阅读检测文章-已推送微信,请40s内完成验证!")
                check = check_status(ck['ts'],result['data']['url'],i)
                if check:
                    print(f"账号【{i+1}】检测文章-过检测成功啦!")
                    result = requests.post(domain+"/r/ck",headers=headers,data="t=quick").json()
                    if result['ret'] == True:
                        count = result['data']['count']
                        print(f"账号【{i+1}】阅读成功-获得[{result['data']['gold']}]积分-已读[{result['data']['count']}]篇")
                    else:
                        print(f"账号【{i+1}】阅读失败,重新获取文章")
                else:
                    print(f"账号【{i+1}】检测文章-过检测失败啦!")
                    break    
            else:
                time.sleep(s)
                result = requests.post(domain+"/r/ck",headers=headers,data="t=quick").json()
                if result['ret'] == True:
                    count = result['data']['count']
                    print(f"账号【{i+1}】阅读成功-获得[{result['data']['gold']}]积分-已读[{result['data']['count']}]篇")
                else:
                    print(f"账号【{i+1}】阅读失败,重新获取文章")
    


# 提现模块
def get_money(i,ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x18002831) NetType/WIFI Language/zh_CN',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://5851751251.fjxsjjw.cn/',
        'Origin': 'http://5851751251.fjxsjjw.cn',
        'a_h_n': f'http%3A%2F%2F5851577307.gbvbmxo.cn%2F%3Fgoid%3Ditrb/{ck["ck"]}' 
    }
    result = requests.post(domain+"/user/getinfo?v=3",headers=headers).json()
    if 'code' not in result:
        pass
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False
    if result['data']['balance']>=Limit*10000:
        tresult = requests.post(domain+"/mine/cash",headers=headers).json()
        if tresult['code'] == 1:
            print(f"账号【{i+1}】金币[{result['data']['balance']}] 已读[{result['data']['count']}]篇 提现成功！")
        else:
            print(f"账号【{i+1}】金币[{result['data']['balance']}] 已读[{result['data']['count']}]篇 提现失败: {tresult['msg']}")
    else:
        print(f"账号【{i+1}】金币[{result['data']['balance']}] 已读[{result['data']['count']}]篇 未达到{Limit}元提现标准!")

# 微信推送模块
def check_status(key,link,index):
    if imei != None:
        if ss.get("https://linxi-send.run.goorm.io").status_code ==200:
            callback = "https://linxi-send.run.goorm.io"
        else:
            callback = "https://auth.linxi.tk"
        result = ss.post(callback+"/create_task",json={"imei":imei}).json()
        uuid = result['uuid']
        print(f"账号【{str(index+1)}】避免并发,本次延迟{index*2}秒,上传服务器[{result['msg']}]")
        time.sleep(index*2)
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-{name}%0A请在{tsleep}秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
        print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
        for i in range(10):
            result = ss.get(callback+f"/select_task/{imei}/{uuid}").json()
            if result['code'] == 200:
                print(f"账号【{str(index+1)}】服务器回调结果:{result['msg']}")
                result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
                print(f"账号【{str(index+1)}】查询本次uuid结果:{result['msg']}")
                return True
            time.sleep(4)
        result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
        print(f"账号【{str(index+1)}】清除本次uuid结果:{result['msg']}")
        return False
    else:
        print(f"账号【{str(index+1)}】避免并发同一时间多个推送,本次推送延迟{index*2}秒")
        time.sleep(index*2)
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-{name}%0A请在{tsleep}秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
        print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
        #print(f"手动微信阅读链接: {link}")
        time.sleep(30)
        return True


if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗   ██╗██████╗ ███████╗
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗ ██╔╝██╔══██╗╚══███╔╝
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚████╔╝ ██║  ██║  ███╔╝ 
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝ ╚██╔╝  ██║  ██║ ███╔╝  
███████╗██║██║ ╚████║██╔╝ ██╗██║        ██║   ██████╔╝███████╗
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝
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
    print("==================回调服务器状态=================")
    if imei:
        print(f"[回调服务器]:已启用-[授权ID:{imei}]")
    else:
        print(f"[回调服务器]:未启用-[变量ID:{imei}]")
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
