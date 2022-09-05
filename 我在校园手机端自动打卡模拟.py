import requests
import json
def main():
    header={"Host": "gw.wozaixiaoyuan.com",#此header为小黄鸟抓包得到的http传输中的header 作用是伪装模拟
            "Connection": "keep-alive",
            "Content-Length": "301",
            "Accept": "application/json, text/plain, */*",
            "JWSESSION": "ee00270689a14df5945c78e45287aab3",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2102K1AC Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/9996 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Content-Type":"application/json;charset=UTF-8",
            "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id=5600001",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
    dk_url="https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch=5600001"#此url是抓包得到的打卡终点链接，最终数据交互通过此链接
    body={"location":"中国/四川省/成都市/新津区/花源街道/SWPU/156/510118/156510100/510118004",#此处为需要交互的数据
          "t1":"[\"无下列情况\"]",
          "t2":"无不适症状",
          "t3":"暑假已离校",
          "t4":"未列为风险区",
          "t5":"正常",
          "t6":"安全",
          "t7":"已全部接种（含加强针）",
          "type":0,
          "locationType":0}
    r=requests.post(url=dk_url,data=json.dumps(body),headers=header)
    print(r)
if __name__=="__main__":
    main()