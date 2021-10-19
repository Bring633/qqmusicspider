# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:23:25 2020

@author: MSI-NB
"""

import requests
import urllib
import json
import re
import socket

#初始化请求的USERAGENCY
headersList = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

#构建请求头
headers = {
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'
        }

# [定义获取页面的函数]

def web_scratch(url,headers = headers,method = 'get',auth = None,cookies = None):
    request_Initial = requests.Request(url = url,method = method,headers = headers,auth = None,cookies = None) #构建一个Resquest对象储存数值
    s = requests.session()#创建一个session对象来解决多会话的问题
    sPrepared = s.prepare_request(request_Initial)#创建一个PreparedRequest对象（可以理解为合并session和Resquest 的功能
    try:
        webInitialCrap = s.send(sPrepared,timeout = 30)#向服务器发送请求，设置一个30s值，超过30s不响应抛出异常
    except urllib.error.URLerror as ure:#捕捉异常
            print(ure.reason)
            if isinstance(ure.reason,socket.timeout):
                print('TIME OUT')
    return webInitialCrap


#[定义获取音乐的内容]
#给函数传递经过处理的列表和索引的页面    

def get_music_info(dataSearchThoughSinger,page):
    midVal = dataSearchThoughSinger
    
    
    for i in range(len(midVal)):
        songData.append([])#创建二维列表

    for i in range(len(midVal)):
        
        dataToSearch = midVal[i]
        albumName = dataToSearch['albumname']
        songMid = dataToSearch['songmid']
        songName = dataToSearch['songname']
        singerName = dataToSearch['singer'][0]['name']

        listToAdd = songData[i+page]#按页来获取时，在添加数据时要根据此来改变选取列表中元素
        listToAdd.append(songMid)
        listToAdd.append(songName)
        listToAdd.append(singerName)
        listToAdd.append(albumName)
        
        songMidList.append(songMid)


#定义下载函数
def music_download(songMid,i,uin,guid):
    uin = '84165801'#必须要qq号才能获取guid
    guid = '1585890083908'#登录后的qq音乐网页中的musics.fcg?g_tk中找


    keyDownLink = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}'%(guid,guid,songMid,uin,uin)
    keyDownLink = web_scratch(keyDownLink)
    vkeyData = json.loads(keyDownLink.text)

    vkey = vkeyData['req_0']['data']['midurlinfo'][0]['purl']
    if vkey is None:#当选取的音乐是vip音乐时，返回的vkey是一个空的列表
        print('这是vip音乐，无法下载')
        pass
    musicDownLoadLink = 'https://isure.stream.qqmusic.qq.com/%s'%(vkey)
    print(musicDownLoadLink)

    data = web_scratch(musicDownLoadLink)
    name = r"C:\Users\MSI-NB\Desktop\musicdownload\{}{}{}.mp3".format(songData[i][1],songData[i][2],songData[i][0])#设置保存的路径和文件名
    
# test file   name = r"C:\Users\MSI-NB\Desktop\musicdownload\1.mp3"
    
#检查文件命名

    nameCheck = name
    nameCheck = re.match(r'.+([\?\*\"\<\>\|]).+',nameCheck)#检查文件的命名，win系统不允许列表中的字符存在
    
    
    if nameCheck is None:
    
        file = open(name,'wb')
        file.write(data.content)
        file.close()
        print(name+'下载成功')
    else:
        intab = "?*/|><"
        outtab = "      "
        trantab = str.maketrans(intab, outtab)#建立字符之间的映射
        name = name.translate(trantab)#转换字符
        file = open(name,'wb+')
        file.write(data.content)
        file.close()
        print(name+'下载成功')