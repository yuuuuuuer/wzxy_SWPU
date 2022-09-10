import requests
import json
from sys import exit
header={"Host": "gw.wozaixiaoyuan.com",#此header为小黄鸟抓包得到的http传输中的header 作用是伪装模拟
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "JWSESSION": open('JWSESSION.txt','r').read(),#从文件中读取
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2102K1AC Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/9996 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64",
            "Content-Type":"application/json;charset=UTF-8",
            #"Referer": "https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}
dk_id='0'#此处是打卡的学校校区ID。稍后会调用函数获取

def GetState():#这个函数调用来测试当前储存的JWSESSION是否过期
    header['Content-Length']='2'
    header['JWSESSION']=open('JWSESSION.txt').read()
    body={}
    header['Referer']="https://gw.wozaixiaoyuan.com/h5/mobile/basicinfo/index/home/homeStudent"
    r=requests.post(url='https://gw.wozaixiaoyuan.com/basicinfo/mobile/home/getHomeApps?env=3',data=json.dumps(body),headers=header).text
    if(json.loads(r)['code']==103):#103代表未登录 JWSESSION过期
        return False
    else:return True
def login():
    username=open('username.txt','r').read()
    password=open('password.txt','r').read()
    login_url=f"https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username?username={username}&password={password}"#此处为登录接口，将账号密码作为参数构造而来
    header['Content-Length']="2"
    body={}#这个body必须有，测试发现不提交就不能成功登录  尽管它并没有内含任何数据
    response=requests.post(url=login_url,data=json.dumps(body),headers=header)#这里的body需要调用json库先编码再提交，二者缺一不可。然后返回一个response对象 对应的是json格式
    if(json.loads(response.text)["code"]==0):#code为0则登陆成功 此处调用json库将数据解码为python字典格式，更方便这里的判断语句
        file=open('JWSESSION.txt','w')#打开文件，使用覆盖写模式
        file.write(response.headers["JWSESSION"]) #将获取到的JWSESSION参数覆盖写入文件
        header['JWSESSION']=response.headers["JWSESSION"]#顺便在这里就将新的JWSESSION写入内存header字典中
        file.close()#关闭文件
        return True
    elif(json.loads(response.text)['code']==101):#101表示账号密码错误
        print ("用户名或密码错误，请检查")
    else:
        print("未知错误")
    exit()#登陆失败 直接退出程序 反正后面也没办法进行打卡了

def GetId():#此处为登录后获取健康打卡学校ID的函数
    if('Content-Length' in header):    
        header.pop("Content-Length")#获取列表的接口没有传输数据 header中也没有长度参数 因此需要弹出可能存在的content-length参数
    get_url="https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch"
    header['Referer']="https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health"
    response=requests.get(url=get_url,headers=header).text#返回一个response对象 内含有打卡列表 获取其text内容
    global dk_id
    dk_id=json.loads(response)["data"]["list"][0]["id"]#这里的id就是学校校区的代码，是打卡接口的构成参数
    #return (dk_id)#将获取到的ID返回给调用对象

def GetForm():#此函数作用是获取打卡的选项并选择答案
    if('Content-Length' in header):    
        header.pop("Content-Length")
    form_url=f"https://gw.wozaixiaoyuan.com/health/mobile/health/getForm?batch={dk_id}"
    header["Referer"]=f"https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id={dk_id}"
    response=requests.get(url=form_url,headers=header).text
    res={"location":"中国/四川省/成都市/新津区/花源街道/SWPU/156/510118/156510100/510118004"}#初始化一个res字典 马上派上用场
    if(json.loads(response))['code']==0:#0代表获取成功
        options=json.loads(response)['data']['options']
        for number in options:
            for objects in options[number]:
                if objects['type']==0 or objects['type']==2:#type为0则在客户端对应的是绿色的答案，优先选择。为2则是黑色答案 随便选 这里默认选第一个
                    res[number]=objects['value']#这样就能建立一个问题id:正确答案 的字典
                    break
        answers={"location":"中国/四川省/成都市/新津区/花源街道/SWPU/156/510118/156510100/510118004",
                 "type":0,#此处两行的type 和locationtype暂时不清楚是做什么的。
                 "locationType":0}
        fields=json.loads(response)['data']['fields']
        for parts in fields:
            if parts['id']!='0' and parts['optionId'] in res.keys():
                answers[parts['field']]=res[parts['optionId']]
        answers['t1']="[\""+ answers['t1'] +"\"]"#这里多此一举是因为抓包发现 只有t1参数是这样的格式 其他的都是直接一个双引号就结束
        return answers

def main():

    dk_url="https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch="#此url是抓包得到的打卡链接，最终数据交互通过此链接，目前还差一个ID参数在末尾 稍后获取
    if(GetState()==False):#首先调用GetState()函数测试当前储存的JWSESSION是否有效 无效返回False 重新登陆
        login()
    GetId()#调用此函数获取打卡学校ID
    
    body=GetForm()#调用函数获取健康打卡的选项
    dk_url=dk_url+dk_id#url+ID  构成最终的打卡链接
    header["Content-Length"]="301"
    header["Referer"]=f"https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id={dk_id}"
    r=requests.post(url=dk_url,data=json.dumps(body),headers=header)#此处的body要用json库进行dumps是因为前面抓包得到的header"Contene-Type"参数是json,意味着此时交换数据采用json格式.
    if(json.loads(r.text)["code"]==0):#为0则打卡成功
            print("OK!")#反馈正确
    elif(json.loads(r.text)["code"]==1):#为1表示打卡时间未开始
            print("打卡时间未开始，打卡失败")
    else:
        print("未知错误")
if __name__=="__main__":
    main()
