# 人人帮阅读
# 入口:http://redpage230617.read.biwuzhaojin.com/web-read/read?channelId=230327002

import requests
import json
import os
import re
import time
import random
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
# Limit = 0
# 人人帮阅读域名(无法使用时请更换)
domain = 'http://ebb.vinse.cn/api'

check_list=['Mzg2Mzk3Mjk5NQ==']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309062f) XWEB/8379 Flue',
    'Referer': 'http://ebb10.twopinkone.cloud/',
    'Content-Type':'application/json; charset=UTF-8',
}

def user_info(i,ck):
    headers['un'] = ck['un']
    headers['uid'] = ck['uid']
    headers['token'] = ck['ck']
    ss = requests.session()
    result = ss.post(domain+"/user/sign", headers=headers, json={"pageSize": 10}).json()
    if result['code'] == 0:
        # print(f"账号【{i+1}】签到成功,获得{result['result']['point']}帮豆!")
        result = ss.post(domain+'/user/receiveOneDivideReward', headers=headers, json={"pageSize": 10}).json()
        # print(f"账号【{i+1} 领取一级帮豆:{result['msg']}")
        result = ss.post(domain+'/user/receiveTwoDivideReward', headers=headers, json={"pageSize": 10}).json()
        # print(f"账号【{i+1} 领取二级帮豆:{result['msg']}")
        result = ss.post(domain+"/user/info", headers=headers, json={"pageSize": 10}).json()
        nick_name = result['result']['nickName']
        money = result['result']['integralCurrent']
        print(f"账号【{i+1}】用户: {nick_name} 帮豆: {money}")
        ss.close
    else:
        ss.close
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False



def do_read(i,ck):
    headers['un'] = ck['un']
    headers['uid'] = ck['uid']
    headers['token'] = ck['ck']
    ss = requests.session()
    result=ss.get(f"https://u.cocozx.cn/ipa/read/getEntryUrl?fr=ebb0726&uid={ck['uid']}",headers=headers).json()
    link=result['result']['url']
    if link==None or link=='':
        print(f"账号【{i+1}】获取阅读链接失败:{result}")
        return False
    mr = re.findall('//mr(.*?)\.', link)[0]
    result = ss.post(f"http://u.cocozx.cn/api/common/ustr?t={mr}", headers=headers,json={"pageSize":20}).json()
    link=result['result']['str']
    if link==None or link=='':
        print(f"账号【{i+1}】获取阅读链接失败:{result}")
        return False
    group = re.findall('&group=(.*?)endok', link+'endok')[0]
    while True:
        data = {"fr":"ebb0726","uid":ck['uid'],"group":group,"un":None,"token":None,"pageSize":20}
        result = ss.post('http://u.cocozx.cn/ipa/read/read', headers=headers, json=data).json()
        if result['code'] == 0:
            status = result['result']['status']
            if status != 10:
                status_list = {30:"未知异常",50:"阅读已黑号",80:"阅读已黑号"}
                if status in list(status_list.keys()):
                    print(f"账号【{i+1}】{status_list[status]}:{result}")
                else:
                    print(f"账号【{i+1}】未收录异常:{result}")
                break
            link = result['result']['url']
            l_result = ss.get(link,headers=headers).text
            # 获取biz
            biz = re.findall("biz=(.*?)&amp;",l_result)
            if biz == []:
                print(f'账号【{i+1}】未找到BIZ,重新获取')
                print(link)
                continue
            else:
                biz = biz[0]
            s = random.randint(7, 10)
            print(f"账号【{i+1}】获取文章成功-{biz}-模拟{s}秒")
            if biz in check_list:
                    print(f"账号【{i+1}】阅读检测文章-已推送微信,请40s内完成验证!")
                    # 过检测
                    check = check_status(ck['ts'],link,i)
                    if check == True:
                        result = ss.post('http://u.cocozx.cn/ipa/read/submit', headers=headers, json=data).json()
                        if result['code'] == 0:
                            print(f"账号【{i+1}】阅读文章成功-获得帮豆[200]-剩余{result['result']['progress']}篇")
                            if result['result']['progress'] > 0:
                                pass
                            else:
                                print(f"账号【{i+1}】本轮阅读已成功")
                                break
                        else:
                            print(f"账号【{i+1}】阅读异常,尝试重新阅读")
                    else:
                        print(f"账号【{i+1}】检测文章-过检测失败啦!")
                        break
            else:
                time.sleep(s)
                result = ss.post('http://u.cocozx.cn/ipa/read/submit', headers=headers, json=data).json()
                if result['code'] == 0:
                    print(f"账号【{i+1}】阅读文章成功-获得帮豆[200]-剩余{result['result']['progress']}篇")
                    if result['result']['progress'] > 0:
                        pass
                    else:
                        print(f"账号【{i+1}】本轮阅读已成功")
                        break
                else:
                    print(f"账号【{i+1}】阅读异常,尝试重新阅读")
    ss.close
                    


def get_money(i,ck):
    headers['un'] = ck['un']
    headers['uid'] = ck['uid']
    headers['token'] = ck['ck']
    result = requests.post(domain+"/user/info", headers=headers, json={"pageSize": 10}).json()['result']
    options = [0.3, 1, 5, 10]  # 可选的数字列表
    max_money = max(filter(lambda x: x < (int(result['integralCurrent'])/10000), options), default=0.3)
    result = requests.post("http://ebb.vinse.cn/apiuser/aliWd", headers=headers, json={"val": max_money, "pageSize": 10}).json()
    if result['code'] == 0 :    
        print(f"账号【{i+1}】提现成功 {result}")
    else:
        print(f"账号【{i+1}】提现失败 {result}")

# 微信推送模块
def check_status(key,link,index):
    print(f"账号【{str(index+1)}】避免并发同一时间多个推送,本次推送延迟{index*2}秒")
    time.sleep(index*2)
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-钢镚阅读%0A请在60秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
    print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
    # print(f"手动微信阅读链接: {link}")
    time.sleep(30)
    return True


if __name__ == "__main__":
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗      ██████╗ ██████╗ ██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔══██╗██╔══██╗██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██████╔╝██████╔╝██████╔╝
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔══██╗██╔══██╗██╔══██╗
███████╗██║██║ ╚████║██╔╝ ██╗██║      ██║  ██║██║  ██║██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
    项目:人人帮(0.5)       BY-林夕       Verion: 0.0.1(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv('rrbtoken') == None:
            print('账号Cookie异常: 请添加rrbtoken变量示例:{"un":"xxx","uid":"123456","ck":"xxxx","ts":"UID_sddsddsd"}')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('rrbtoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"un":"xxx","uid":"123456","ck":"xxxx","ts":"UID_sddsddsd"}
        ]
        if ck_token == []:
            print('账号异常: 请添加本地ck_token示例:{"un":"xxx"x,"uid":"123456","ck":"xxxx","ts":"UID_sddsddsd"}')

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

        # 输出结果
        print("================[人人帮V0.0.2]===============")
