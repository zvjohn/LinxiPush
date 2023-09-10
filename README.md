# LinxiPush(`林夕微信推送助手V1.0`)
## 注：更新钢镚、小阅阅读并发版本con.py（检测更新为全手动检测30s 无回调服务器支持，可根据自己的账号数量自调check_status函数延迟时间）

## `Wxpusher全自动过检测工具 V1.0`已上传。授权请联系我
### 特此感谢zonghua大佬的开源项目:`https://github.com/zh-h/Windows.Media.Ocr.Cli`
## 提醒: 当前微信测试号关注已达到上限，为此采用`Wxpusher`作为推送备用方案

### `林夕微信推送助手V1.0` 基于Python3 + Flask + 微信测试号,用于为客户发送模板或者图文消息达到消息推送的效果。
> #### `Wxpusher`推送使用示例:
> ```python
> import requests
> import urllib.parse
> wxname = 'xx' # 获取UID 扫码获取 https://wxpusher.zjiecode.com/demo/
> # 微信推送
> def WxSend(project, status, content,turl):
>     turl = urllib.parse.quote(turl)
>     result = requests.get(f'https://wxpusher.zjiecode.com/demo/send/custom/{wxname}?content={status}-{project}%0A{content}%0A%3Cbody+onload%3D%22window.location.href%3D%27{turl}%27%22%3E').json()
>     print(f"微信消息推送: {result['msg']}")
> 
> WxSend("微信阅读-小阅阅读", f"检测文章", "请在60s内阅读当前文章","http://baidu.com")
## 仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
## 您必须在下载后的24小时内从计算机或手机中完全删除以上内容
