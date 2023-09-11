# LinxiPush(`林夕微信推送助手V1.0`)
#### 注：更新钢镚、小阅阅读并发版本con.py（检测更新为全手动检测30s 无回调服务器支持，可根据自己的账号数量自调check_status函数延迟时间）

## 全自动过检测`Wxpusher全自动过检测工具Win10版本 V1.1`已上传。授权请联系我
## 全自动过检测`Wxpusher全自动过检测工具兼容版 V1.1` 全英文路径
#### 特此感谢[@zh-h](https://github.com/zh-h) 大佬的开源项目:[https://github.com/zh-h/Windows.Media.Ocr.Cli](https://github.com/zh-h/Windows.Media.Ocr.Cli)
#### 特此感谢[@benjaminwan](https://gitee.com/benjaminwan) 大佬的开源项目:[https://gitee.com/benjaminwan/ocr-lite-ncnn](https://gitee.com/benjaminwan/ocr-lite-ncnn)
> #### `Wxpusher`推送使用示例:

    import requests
	import urllib.parse
	wxname = 'xxx' # 获取UID 扫码获取 https://wxpusher.zjiecode.com/demo/
	# 微信推送
	def WxSend(project, status, content,turl):
    	turl = urllib.parse.quote(turl)
    	result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{wxname}?content={status}-{project}%0A{content}%0A%3Cbody+onload%3D%22window.location.href%3D%27{turl}%27%22%3E').json()
    	print(f"微信消息推送: {result['msg']}")

	WxSend("微信阅读-测试阅读", f"检测文章", "请在60s内阅读当前文章","http://baidu.com")
> #### `Wxpusher自动检测助手`使用示例:
> 请查看压缩包内使用文档!!!!
## 仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
## 您必须在下载后的24小时内从计算机或手机中完全删除以上内容
