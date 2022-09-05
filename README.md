# wzxy_SWPU
我在校园每日自动健康打卡（粗略版）
使用方法：通过手机小黄鸟抓包，从抓到的header中获取JWSESSION参数内容。再将其填入源码中的JWSESSION一行。
目前尚不清楚JWSESSION的更新时效是多久， 至于为什么不用fiddler搭配PC端，是因为昨日抓包发现两个问题，一是微信小程序组件更新，导致出现fiddler抓不到小程序的包，其次是我在校园疑似修改了机制，不允许PC端使用。

tips：目前只是粗糙半成品。如果不出意外，各位抓包得到的数据中，进行提交打卡的链接url应当是：
https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch=5600001
url末尾的5600001作用存疑，目前怀疑是对应健康打卡这一项的内部ID，而不是每个用户对应的ID。

小黄鸟下载地址链接：https://pan.baidu.com/s/18VEpucY-mqsReWggCfmUQQ 
提取码：6666
使用非常简单。因此就不另作说明了。
如果有其余的问题，请各位朋友留言指教 或者私聊均可， 不过目前本人尚不熟悉GitHub的相关功能...




实现原理：模拟网页HTTP协议直接调用接口进行数据交换。
源码调用两个库：post（第三方库，需要使用pip install post获取） 作用是模拟http发送post指令
              json（标准库）作用是在发送post指令的过程中将数据编码成json格式
header头的作用：定义一些属性，用于告诉浏览器具体做什么以及有什么。 例如"Content-Type":"application/json;charset=UTF-8" 指的是使用json交换数据;编码使用UTF-8标准。
在这个源码中添加header包含的各项的作用是——伪装成合法的http请求。例如"User-Agent"这一行包含的信息就有设备信息，我在校园小程序也应当是由此判断用户是PC端还是手机端。

body中包含的信息很显然是需要传入我在校园打卡的数据。我所在的学校每日打卡需要的数据只有八项，因此抓包得到的body内容也只有这几项。不同的学校可能有所不同，因此各位朋友需要视情况来修改body的信息。
