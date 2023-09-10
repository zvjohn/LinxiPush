# Author: lindaye
# V1.1.6 Update:2023-09-10
# 活动入口：https://sd8690.viptaoyou.top:10261/yunonline/v1/auth/1c3da9bd1689d78a51463138d634512f?codeurl=sd8690.viptaoyou.top:10261&codeuserid=2&time=1694212129
# 变量xyytoken 值{"ck":"ysm_uid的值","ts":"Wxpusher的UID"} 一行一个
# 内置ck方法ck_token = [{"ck":"ysm_uid的值","ts":"Wxpusher的UID"},{"ck":"ysm_uid的值","ts":"Wxpusher的UID"}]
# 扫码关注wxpusher获取UID: https://wxpusher.zjiecode.com/demo/
import requests
import json
import time
import random
import re
import os
from multiprocessing import Pool
from urllib.parse import unquote,quote

domain = 'http://1694168723.yxdl444.top'

check_list = [
    "MzkxNTE3MzQ4MQ==","Mzg5MjM0MDEwNw==","MzUzODY4NzE2OQ==","MzkyMjE3MzYxMg==","MzkxNjMwNDIzOA==","Mzg3NzUxMjc5Mg==",
    "Mzg4NTcwODE1NA==","Mzk0ODIxODE4OQ==","Mzg2NjUyMjI1NA==","MzIzMDczODg4Mw==","Mzg5ODUyMzYzMQ==","MzU0NzI5Mjc4OQ==",
    "Mzg5MDgxODAzMg==",
]

def ts ():
    return str (int (time .time ()))+'000'

def test(index,ck):
    # 保持连接,重复利用
    ss = requests.session()
    ysm_uid = ck['ck']
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380',
        'Cookie':f"ysm_uid={ck['ck']}"
    }
    result = ss.get(domain,headers=headers).text
    signid = re.findall(r'id\'\) \|\| "(.*?)";',result)
    if signid == []:
        print (f'当前账号【{str(index+1)}】:初始化失败,请检测CK({ck['ck']})是否正确!')
        return False
    else:
        print (f'当前账号【{str(index+1)}】:初始化成功,账号登陆成功!')
        result = ss.get(f'{domain}/yunonline/v1/exchange?unionid={ysm_uid}&request_id={signid}&qrcode_number=&addtime=').text
        money = re.findall(r'id="exchange_gold">(.*?)</p>',result)
        if money == []:
            print (f'当前账号【{str(index+1)}】:金币获取失败,账号异常')
        else:
            rmb = re.findall(r'money = (.*?);',result)[0]
            if int(money[0]) >= 3000:
                money = (int(money[0]) // 3000) * 3000
                print(f"当前账号【{str(index+1)}】:提交体现金币: {money}")
                t_data = {'unionid':ysm_uid,'request_id':signid,'gold':money}
                t_result = ss.post(f'{domain}/yunonline/v1/user_gold',json=t_data).json()
                if t_result['errcode'] == 0:
                    print(f"当前账号【{str(index+1)}】金币转金额成功: {t_result['data']['money']} 当前余额:{rmb}")
                else:
                    print(f"当前账号【{str(index+1)}】金币转金额失败: {t_result['msg']} 当前余额:{rmb}")
                if rmb >= "2.0":
                    j_data = {'unionid':ysm_uid,'signid':signid,'ua':0,'ptype':0,'paccount':'','pname':''}
                    j_result = ss.post(f'{domain}/yunonline/v1/withdraw',data=j_data).json()
                    print(f"当前账号【{str(index+1)}】体现结果: {j_result['msg']}")
                else:
                    print(f"当前账号【{str(index+1)}】余额小于2元暂不提现!")
            else:
                print(f'当前账号【{str(index+1)}】还未到达提现最低金币 当前金币: {money[0]} 当前余额:{rmb}')
        result = ss.get(f'{domain}/yunonline/v1/sign_info?time={ts()}000&unionid={ysm_uid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'当前账号【{str(index+1)}】:获取用户信息失败，账号异常')
        result = ss.get(f'{domain}/yunonline/v1/hasWechat?unionid={ysm_uid}').json()
        if result['errcode'] == 0:
            pass
        else:
            print (f'当前账号【{str(index+1)}】:获取用户信息失败，账号异常')
        result = ss.get(f'{domain}/yunonline/v1/gold?unionid={ysm_uid}&time={ts()}000').json()
        if result['errcode'] == 0:
            print(f"当前账号【{str(index+1)}】:今日积分: {result['data']['day_gold']} 已阅读: {result['data']['day_read']}篇 剩余: {result['data']['remain_read']}篇")
        else:
            print (f'当前账号【{str(index+1)}】:获取用户信息失败，账号异常')
        data = {'unionid':ysm_uid}
        result = ss.post(f'{domain}/yunonline/v1/wtmpdomain',json=data).json()
        uk = re.findall(r'uk=([^&]+)',result['data']['domain'])[0]
        print(f"获取到KEY: {uk}")
        while True:
            result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}').json()
            if result['errcode'] == 0:
                link = result['data']['link']
                l_result = ss.get(link,headers=headers).text
                # 获取biz
                biz = re.findall("biz=(.*?)&amp;",l_result)
                if biz == []:
                    print(f'当前账号【{str(index+1)}】:未找到BIZ,重新获取')
                    continue
                else:
                    biz = biz[0]
                s = random.randint(6,8)
                print (f'当前账号【{str(index+1)}】:获取文章成功-{biz}-本次模拟读{s}秒')
                if biz in check_list:
                    print(f"当前账号【{str(index+1)}】:阅读文章检测-已推送至微信,请60s内完成验证!")
                    #print(f"获取到微信文章: {link}")
                    link = re.findall('_g.msg_link = "(.*?)"',l_result)[0]
                    # 过检测
                    check = check_status(ck['ts'],link,index)
                    if check == True:
                        print(f"当前账号【{str(index+1)}】:检测文章-过检测成功啦!")
                        r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                        if r_result['errcode'] == 0:
                            print(f"当前账号【{str(index+1)}】阅读已完成: 获得{r_result['data']['gold']}积分")
                        else:
                            print(r_result)
                            break
                    else:
                        print(f"当前账号【{str(index+1)}】:检测文章-过检测失败啦!")
                        break
                else:
                    time.sleep(s)
                    r_result = ss.get(f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={s}&timestamp={ts()}').json()
                    if r_result['errcode'] == 0:
                        print(f"当前账号【{str(index+1)}】阅读已完成: 获得{r_result['data']['gold']}积分")
                    else:
                        print(f"当前账号【{str(index+1)}】:阅读失败,获取到未收录检测BIZ:{biz}")
                        print(r_result)
                        break
            else:
                if result['msg'] == "任务重复" or result['msg'] == "任务超时":
                    print(f"当前账号【{str(index+1)}】:阅读失败: {result['msg']}重新获取文章")
                else:
                    print (f"当前账号【{str(index+1)}】:阅读提醒: {result['msg']}")
                    break
    ss.close

def check_status(key,link,index):
    time.sleep(index)
    result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-小阅阅读%0A请在60秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
    print(f"微信消息推送: {result['msg']}")
    print(f"手动微信阅读链接: {link}")
    time.sleep(60)
    return True


if __name__ == '__main__':
    print("""██╗     ██╗███╗   ██╗██╗  ██╗██╗     ██╗  ██╗██╗   ██╗██╗   ██╗██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║     ╚██╗██╔╝╚██╗ ██╔╝╚██╗ ██╔╝██╔══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗╚███╔╝  ╚████╔╝  ╚████╔╝ ██║  ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██╔██╗   ╚██╔╝    ╚██╔╝  ██║  ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║     ██╔╝ ██╗   ██║      ██║   ██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═════╝ 
                    BY-林夕               Verion: 1.1.7(并发)
""")

    if os.getenv('xyytoken') == None:
        print("账号Cookie异常: 请添加xyytoken变量!")
        exit()
    # CK列表
    ck_token = [json.loads(line) for line in os.getenv('xyytoken').splitlines()]
    # 创建进程池，默认会根据系统的CPU核心数创建相应数量的进程
    with Pool() as pool:
        # 使用enumerate函数获取每个ID在列表中的索引，并与ID值一起作为参数传递给test函数
        # 使用map方法将每个元组作为参数提交到进程池中
        pool.starmap(test, list(enumerate(ck_token)))
        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完成
        pool.join()
