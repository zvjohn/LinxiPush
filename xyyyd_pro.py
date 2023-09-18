# Author: lindaye
# Update:2023-09-17
# 活动入口：https://sd8690.viptaoyou.top:10261/yunonline/v1/auth/1c3da9bd1689d78a51463138d634512f?codeurl=sd8690.viptaoyou.top:10261&codeuserid=2&time=1694212129
# 变量xyytoken 值{"ck":"ysm_uid的值","ts":"Wxpusher的UID"} 一行一个
# 内置ck方法ck_token = [{"ck":"ysm_uid的值","ts":"Wxpusher的UID"},{"ck":"ysm_uid的值","ts":"Wxpusher的UID"}]
# 开启devid设备id变量值为{"ck":"ysm_uid的值","ts":"Wxpusher的UID","did":"xxxx"}
# 先扫码关注wxpusher获取UID: https://wxpusher.zjiecode.com/demo/
# 回调服务器：青龙运行填写imei变量,本地运行修改imei = ""为真实设备ID
import requests
import json
import time
import random
import re
import os
from multiprocessing import Pool
from urllib.parse import quote

# 变量类型(本地/青龙)
Btype = "青龙"
# 提现限制(元)
Limit = 2
# 授权设备ID
imei = os.getenv('LID')
# 小阅阅读域名(无法使用时请更换)
domain = 'http://1692416143.3z2rpa.top'
# 检测文章列表(如有未收录可自行添加)
check_list = [
    "MzkxNTE3MzQ4MQ==","Mzg5MjM0MDEwNw==","MzUzODY4NzE2OQ==","MzkyMjE3MzYxMg==","MzkxNjMwNDIzOA==","Mzg3NzUxMjc5Mg==",
    "Mzg4NTcwODE1NA==","Mzk0ODIxODE4OQ==","Mzg2NjUyMjI1NA==","MzIzMDczODg4Mw==","Mzg5ODUyMzYzMQ==","MzU0NzI5Mjc4OQ==",
    "Mzg5MDgxODAzMg==",
]
# 时间戳
def ts ():
    return str (int (time .time ()))+'000'

# 获取个人信息模块
def user_info(i,ck):
    # 保持连接,重复利用
    ss = requests.session()
    ysm_uid = ck['ck']
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380',
        'Cookie':f"ysm_uid={ysm_uid}"
    }
    result = ss.get(domain,headers=headers).text
    signid = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if signid == []:
        print (f'账号【{i+1}】初始化失败,请检测CK({ck["ck"]})是否正确!')
        return False
    else:
        result = ss.get(f'{domain}/yunonline/v1/sign_info?time={ts()}000&unionid={ysm_uid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False
        result = ss.get(f'{domain}/yunonline/v1/hasWechat?unionid={ysm_uid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False
        result = ss.get(f'{domain}/yunonline/v1/gold?unionid={ysm_uid}&time={ts()}000').json()
        if result['errcode'] == 0:
            print(f"账号【{i+1}】今日积分: {result['data']['day_gold']} 已阅读: {result['data']['day_read']}篇 剩余: {result['data']['remain_read']}篇")
        else:
            print (f'账号【{i+1}】获取用户信息失败，账号异常:{result}')
            return False

# 阅读文章模块
def do_read(i,ck):
    # 保持连接,重复利用
    ss = requests.session()
    if 'did' in ck:
        Did_data=f"unionid={ck['ck']}&devid={ck['did']}"
        Did_R = ss.post( domain+'/yunonline/v1/devtouid',data=Did_data)
        print(f"账号【{i+1}】模拟上传设备指纹: {ck['did']}")
    data = {'unionid':ck['ck']}
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380',
        'Cookie':f"ysm_uid={ck['ck']}"
    }
    result = ss.post(f'{domain}/yunonline/v1/wtmpdomain',json=data).json()
    uk = re.findall(r'uk=([^&]+)',result['data']['domain'])[0]
    print(f"账号【{i+1}】获取到KEY: {uk}")
    while True:
            result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}').json()
            if result['errcode'] == 0:
                link = result['data']['link']
                l_result = ss.get(link,headers=headers).text
                # 获取biz
                biz = re.findall("biz=(.*?)&amp;",l_result)
                if biz == []:
                    print(f'账号【{i+1}】未找到BIZ,重新获取')
                    print(link)
                    continue
                else:
                    biz = biz[0]
                s = random.randint(6,8)
                print (f'账号【{i+1}】获取文章成功-{biz}-模拟{s}秒')
                if biz in check_list:
                    print(f"账号【{i+1}】阅读检测文章-已推送微信,请40s内完成验证!")
                    #print(f"获取到微信文章: {link}")
                    link = re.findall('_g.msg_link = "(.*?)"',l_result)[0]
                    # 过检测
                    check = check_status(ck['ts'],link,i)
                    if check == True:
                        print(f"账号【{i+1}】检测文章-过检测成功啦!")
                        r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                        if r_result['errcode'] == 0:
                            print(f"账号【{i+1}】阅读已完成: 获得{r_result['data']['gold']}积分 剩余{r_result['data']['remain_read']}篇")
                        elif r_result['msg'] == "本次阅读无效":
                            print(f"账号【{i+1}】检测异常重新获取:{r_result}")
                        else:
                            print(f"账号【{i+1}】检测异常:{r_result}")
                            break
                    else:
                        print(f"账号【{i+1}】检测文章-过检测失败啦!")
                        break
                else:
                    time.sleep(s)
                    r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                    if r_result['errcode'] == 0:
                        print(f"账号【{i+1}】阅读已完成: 获得{r_result['data']['gold']}积分 剩余{r_result['data']['remain_read']}篇")
                    else:
                        print(f"账号【{i+1}】阅读失败,获取到未收录检测BIZ:{biz}")
                        print(f"账号【{i+1}】阅读异常:{r_result}")
                        break
            else:
                if result['msg'] in ["任务重复","任务超时","阅读无效"]:
                    print(f"账号【{i+1}】阅读失败: {result['msg']}重新获取文章")
                else:
                    print (f"账号【{i+1}】阅读提醒: {result['msg']}")
                    break
    ss.close


# 提现模块
def get_money(i,ck):
    # 保持连接,重复利用
    ss = requests.session()
    ysm_uid = ck['ck']
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380',
        'Cookie':f"ysm_uid={ysm_uid}"
    }
    result = ss.get(domain,headers=headers).text
    signid = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if signid == []:
        print (f'账号【{i+1}】初始化失败,请检测CK({ck["ck"]})是否正确!')
        return False
    else:
        result = ss.get(f'{domain}/yunonline/v1/exchange?unionid={ysm_uid}&request_id={signid}&qrcode_number=&addtime=').text
        money = re.findall(r'id="exchange_gold">(.*?)</p>',result)
        if money == []:
            print (f'账号【{i+1}】金币获取失败,账号异常')
        else:
            money = money[0]
            rmb = re.findall(r'money = (.*?);',result)[0]
            if int(money) >= 3000:
                tmoney = (int(money) // 3000) * 3000
                # print(f"账号【{i+1}】提交体现金币: {tmoney}")
                t_data = {'unionid':ysm_uid,'request_id':signid,'gold':tmoney}
                t_result = ss.post(f'{domain}/yunonline/v1/user_gold',json=t_data).json()
                money = int(money) - 3000
            if float(rmb) >= float(Limit):
                j_data = {'unionid':ysm_uid,'signid':signid,'ua':0,'ptype':0,'paccount':'','pname':''}
                j_result = ss.post(f'{domain}/yunonline/v1/withdraw',data=j_data).json()
                print(f"账号【{i+1}】余额满足2元体现结果: {j_result['msg']}")
            else:
                print(f"账号【{i+1}】余额小于2元暂不提现! 当前金币: {money} 当前余额:{rmb}")
           

# 微信推送模块
def check_status(key,link,index):
    ss = requests.session()
    if ss.get("https://linxi-send.run.goorm.app").status_code ==200:
        callback = "https://linxi-send.run.goorm.app"
    else:
        callback = "https://auth.linxi.tk"
    if imei != None:
        result = ss.post(callback+"/create_task",json={"imei":imei}).json()
        uuid = result['uuid']
        print(f"账号【{str(index+1)}】避免并发,本次延迟{index*2}秒,上传服务器[{result['msg']}]")
        time.sleep(index*2)
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-钢镚阅读%0A请在60秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
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
        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-小阅阅读%0A请在40秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
        print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
        #print(f"手动微信阅读链接: {link}")
        time.sleep(30)
        return True

if __name__ == "__main__":
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗██╗   ██╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝  ╚████╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗   ╚██╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗   ██║      ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═════╝ 
    项目:小阅阅读                BY-林夕               Verion: 1.1.8(并发)
""")
    if Btype == "青龙":
        if os.getenv('xyytoken') == None:
            print('青龙变量异常: 请添加xyytoken变量示例:{"ck":"xxxx","ts":"UID_xxx"} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv('xyytoken').splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"ck":"xxxxxxx","ts":"UID_xxxxxx"},
            {"ck":"xxxxxxx","ts":"UID_xxxxxx"}
        ]
        if ck_token == []:
            print('本地变量异常: 请添加本地ck_token示例:{"ck":"xxxx","ts":"UID_xxx"}')
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

        # 输出结果
        print("================[小阅阅读V1.1.9]===============")
