import requests
import json
def login():#这个函数的功能就是使用账号密码来登录我在校园，并且获取新的JWSESSION值
    username="xxxxxxx"#这里填写我在校园的账号和密码
    password="xxxxxxx"
    login_url=f"https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username?username={username}&password={password}"#此处为登录接口，将账号密码作为参数构造而来
    header={"Host": "gw.wozaixiaoyuan.com",#此header为小黄鸟抓包得到的http传输中的header 作用是伪装模拟
            "Connection": "keep-alive",
            "Content-Length":"2",
            "Accept": "application/json, text/plain, */*",
            #"JWSESSION": "ee00270689a14df5945c78e45287aab3",这里打注释的参数经过测试发现非必要，可以省去
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2102K1AC Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/9996 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Content-Type":"application/json;charset=UTF-8",
            #"Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/basicinfo/index/login/index?jwcode=10",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    body={}#这个body必须有，测试发现不提交就不能成功登录  尽管它并没有内含任何数据
    response=requests.post(url=login_url,data=json.dumps(body),headers=header)#这里的body需要调用json库先编码再提交，二者缺一不可。然后返回一个response对象 对应的是json格式
    if(json.loads(response.text)["code"]==0):#code为0则登陆成功 此处调用json库将数据解码为python字典格式，更方便这里的判断语句
        file=open('JWSESSION.txt','w')#打开文件，使用覆盖写模式
        file.write(response.headers["JWSESSION"]) #将获取到的JWSESSION参数覆盖写入文件
        file.close()#关闭文件
        return True
    else:return False#登陆失败 返回错误

def main():
    header={"Host": "gw.wozaixiaoyuan.com",#此header为小黄鸟抓包得到的http传输中的header 作用是伪装模拟
            "Connection": "keep-alive",
            "Content-Length": "301",
            "Accept": "application/json, text/plain, */*",
            "JWSESSION": "",#这里初始为空 稍后从文件中读取
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2102K1AC Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/9996 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Content-Type":"application/json;charset=UTF-8",
            "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id=5600001",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    dk_url="https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch=5600001"#此url是抓包得到的打卡终点链接，最终数据交互通过此链接
    body={"location":"中国/四川省/成都市/新津区/花园街道/SWPU/156/510118/156510100/510118004",#此处为需要交互的数据 locaion可以随便填，后面的数字是前面国家/省份/城市/行政区依次对应的编码，测试发现这一行乱填也能打卡成功
          "t1":"[\"无下列情况\"]",
          "t2":"无不适症状",
          "t3":"暑假已离校",
          "t4":"未列为风险区",
          "t5":"正常",
          "t6":"安全",
          "t7":"已全部接种（含加强针）",
          "type":0,#此处两行的type 和locationtype暂时不清楚是做什么的。
          "locationType":0}
    file=open('JWSESSION.txt','r')
    header["JWSESSION"]=file.read()#file文件中保存的即为JWSESSION参数的值 这里用同目录下的txt文件保存
    file.close()
    r=requests.post(url=dk_url,data=json.dumps(body),headers=header)#此处的body要用json库进行dumps是因为前面抓包得到的header"Contene-Type"参数是json,意味着此时交换数据采用json格式.
    if(json.loads(r.text)["code"]==0):#为0则打卡成功
            print("OK!")#反馈正确
    elif(json.loads(r.text)["code"]==1):#为1表示打卡时间未开始
            print("打卡时间未开始，打卡失败")
    elif(json.loads(r.text)["code"]==103):#103代表未登录 意味着JWSESSION已经过期，需要调用login函数来模拟登录 获取新的JWSESSION
        print("Wrong! Updating JWSESSION……")#反馈出错
        if(login()):#为真则login成功  JWSESSION已经重新写入文件
            file=open('JWSESSION.txt')
            header['JWSESSION']=file.read()#读取并更新JWSESSION
            main()#再次调用main函数尝试打卡
        else:
            print("登录账号更新JWSESSION失败 请检查账号密码")
if __name__=="__main__":
    main()
