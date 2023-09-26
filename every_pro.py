# Author: lindaye
# Update:2023-09-26
# 人人帮阅读
# 活动入口：http://ebb.useradmin.cloud/user/index.html?mid=1703917033462300672
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量rrbtoken 值{"un":"xxx","uid":"123456","ck":"token","ts":"Wxpusher的UID"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"un":"xxx","uid":"123456","ck":"token","ts":"Wxpusher的UID"},{"un":"xxx","uid":"123456","ck":"token","ts":"Wxpusher的UID"}]
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
name = "人人帮阅读"
linxi_token = "rrbtoken"
linxi_tips = '{"un":"xxx","uid":"123456","ck":"token","ts":"Wxpusher的UID"}'
import requests
import json
import os
import re
import time
import random
from multiprocessing import Pool
from urllib.parse import quote
# 阅读等待时间
tsleep = 40
# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
Limit = 1
# 授权设备ID(软件版本>=1.3.3)[非授权用户不填即可]
imei = os.getenv('LID')
# 人人帮阅读域名(无法使用时请更换)
domain = 'http://ebb.vinse.cn/api'
# 保持连接,重复使用
ss = requests.session()

check_list=['Mzg2Mzk3Mjk5NQ==']

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5279 MMWEBSDK/20230805 MMWEBID/3850 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
    'platform': '0',
}

def user_info(i,ck):
    headers['un'] = ck['un']
    headers['uid'] = ck['uid']
    headers['token'] = ck['ck']
    result = ss.post(domain+"/user/sign", headers=headers, json={"pageSize": 10}).json()
    if result['code'] != 50 or result['code'] != 4:
        # print(f"账号【{i+1}】签到成功,获得{result['point']}帮豆!")
        result = ss.post(domain+'/user/receiveOneDivideReward', headers=headers, json={"pageSize": 10}).json()
        # print(f"账号【{i+1} 领取一级帮豆:{result['msg']}")
        result = ss.post(domain+'/user/receiveTwoDivideReward', headers=headers, json={"pageSize": 10}).json()
        # print(f"账号【{i+1} 领取二级帮豆:{result['msg']}")
        result = ss.post(domain+"/user/info", headers=headers, json={"pageSize": 10}).json()['result']
        nick_name = result['nickName']
        money = result['integralCurrent']
        print(f"账号【{i+1}】用户: {nick_name} 帮豆: {money}")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")
        return False



def do_read(i,ck):
    try:
        headers['un'] = ck['un']
        headers['uid'] = ck['uid']
        headers['token'] = ck['ck']
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
            time.sleep(3)
            data = {"fr":"ebb0726","uid":ck['uid'],"group":group,"un":None,"token":None,"pageSize":20}
            result = ss.post('http://u.cocozx.cn/ipa/read/read', headers=headers, json=data).json()
            if result['code'] == 0:
                status = result['result']['status']
                if status != 10:
                    status_list = {30:"未知异常",50:"阅读已黑号",60:"你已读完所有推荐文章",80:"阅读已黑号"}
                    if status in list(status_list.keys()):
                        if status == 30:
                            print(f"账号【{i+1}】{status_list[status]}尝试重新获取:{result}")
                        else:
                            print(f"账号【{i+1}】{status_list[status]}")
                            return False
                    else:
                        print(f"账号【{i+1}】未收录异常(垃圾人人帮,快快把钱拿来):{result}")
                else:
                    link = result['result']['url']
                    l_result = ss.get(link,headers=headers).text
                    # 获取biz
                    biz = re.findall("biz=(.*?)&",link)
                    if biz == []:
                        biz = re.findall('_g.msg_link = "(.*?)"',l_result)
                        if biz == []:
                            print(f'账号【{i+1}】未找到BIZ,重新获取')
                            # print(link)
                            continue
                        else:
                            biz = biz[0]
                    else:
                        biz = biz[0]
                    s = random.randint(7, 10)
                    print(f"账号【{i+1}】获取文章成功-{biz}-模拟{s}秒")
                    if biz in check_list:
                            print(f"账号【{i+1}】阅读检测文章-已推送微信,请40s内完成验证!")
                            # 过检测
                            check = check_status(ck['ts'],link,i)
                            if check == True:
                                time.sleep(1)
                                result = ss.post('http://u.cocozx.cn/ipa/read/submit', headers=headers, json=data).json()
                                if result['code'] == 0:
                                    print(f"账号【{i+1}】阅读文章成功-获得帮豆[200]-剩余{result['result']['progress']}篇")
                                    if result['result']['progress'] > 0:
                                        pass
                                    else:
                                        print(f"账号【{i+1}】本轮阅读已成功")
                                        return True
                                else:
                                    print(f"账号【{i+1}】阅读异常,尝试重新阅读")
                            else:
                                print(f"账号【{i+1}】检测文章-过检测失败啦!")
                                return False
                    else:
                        time.sleep(s)
                        result = ss.post('http://u.cocozx.cn/ipa/read/submit', headers=headers, json=data).json()
                        if result['code'] == 0:
                            print(f"账号【{i+1}】阅读文章成功-获得帮豆[200]-剩余{result['result']['progress']}篇")
                            if result['result']['progress'] > 0:
                                pass
                            else:
                                print(f"账号【{i+1}】本轮阅读已成功")
                                return True
                        else:
                            print(f"账号【{i+1}】阅读异常,尝试重新阅读")
            else:
                print(f"账号【{i+1}】获取阅读文章失败:{result['msg']}")
                break
    except requests.exceptions.ConnectionError as e:
        print("网络连接错误超时:", str(e))
                    


def get_money(i,ck):
    headers['un'] = ck['un']
    headers['uid'] = ck['uid']
    headers['token'] = ck['ck']
    result = ss.post(domain+"/user/info", headers=headers, json={"pageSize": 10}).json()['result']
    if result != None:
        options = [5000, 10000, 50000, 100000]  # 可选的金币列表
        max_money = max(filter(lambda x: x < (int(result['integralCurrent'])), options), default=0)
        if max_money >= Limit*10000 :
            result = ss.post("http://ebb.vinse.cn/apiuser/aliWd", headers=headers, json={"val": max_money, "pageSize": 10}).json()
            if result['code'] == 0 :    
                print(f"账号【{i+1}】提现({max_money/10000})成功 {result}")
            else:
                print(f"账号【{i+1}】提现({max_money/10000})失败 {result}")
        else:
            print(f"账号【{i+1}】当前金币[{result['integralCurrent']}] 未到达{Limit}元提现限制!")
    else:
        print(f"账号【{i+1}】账号异常请检查该账号ck是否正确!")

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
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗      ██████╗ ██████╗ ██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔══██╗██╔══██╗██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██████╔╝██████╔╝██████╔╝
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔══██╗██╔══██╗██╔══██╗
███████╗██║██║ ╚████║██╔╝ ██╗██║      ██║  ██║██║  ██║██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
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
        print("==================重复阅读文章=================")
        pool.starmap(do_read, list(enumerate(ck_token)))
        print("==================再次阅读文章=================")
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
