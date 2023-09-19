# LinxiPush(`林夕微信推送助手V1.0`)
#### 注：并发升级版本pro.py（检测更新为全手动检测40s 无回调服务器支持，可根据自己的账号数量自调check_status函数延迟时间）

## 全自动过检测`Wxpusher全自动过检测工具Win10版本 V1.1`已上传。授权请联系我
## 全自动过检测`Wxpusher全自动过检测工具兼容版 V1.1` 全英文路径
#### 特此感谢[@zh-h](https://github.com/zh-h) 大佬的开源项目:[https://github.com/zh-h/Windows.Media.Ocr.Cli](https://github.com/zh-h/Windows.Media.Ocr.Cli)
#### 特此感谢[@benjaminwan](https://gitee.com/benjaminwan) 大佬的开源项目:[https://gitee.com/benjaminwan/ocr-lite-ncnn](https://gitee.com/benjaminwan/ocr-lite-ncnn)
> #### `Wxpusher`推送使用示例(请先用此demo进行测试):

   	import requests
	import time
	from urllib.parse import quote
 
	# 授权用户的LID
	imei = None # imei = "LID"
	UID = "UID_XXXX"
	
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
	                print(result)
	                result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
	                print(result)
	                return True
	            time.sleep(4)
	        result = ss.get(callback+f"/delete_task/{imei}/{uuid}").json()
	        print(result)
	        return False
	    else:
	        print(f"账号【{str(index+1)}】避免并发同一时间多个推送,本次推送延迟{index*2}秒")
	        time.sleep(index*2)
	        result = ss.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{key}?content=检测文章-小阅阅读%0A请在40秒内完成验证!%0A%3Cbody+onload%3D%22window.location.href%3D%27{quote(link)}%27%22%3E').json()
	        print(f"账号【{str(index+1)}】微信消息推送: {result['msg']},等待40s完成验证!")
	        #print(f"手动微信阅读链接: {link}")
	        time.sleep(30)
	        return True
	
	check = check_status(UID,"http://baidu.com",1)
	print(check)
> #### `Wxpusher自动检测助手`使用示例:
> 请查看压缩包内使用文档!!!!

> 打赏

## 仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
## 您必须在下载后的24小时内从计算机或手机中完全删除以上内容
