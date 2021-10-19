# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:39:55 2020

@author: MSI-NB
"""
import urllib
import requests
import socket
import json
import re
import pymysql

#%%
#初始化数据库

dbConnect = input('是否连接数据库（yes，no)')

if dbConnect == 'yes':
    user = input('请输入数据库用户名')
    password = input('请输入数据库用户的密码')
    port = int(input('请输入端口'))
    db = input('请输入数据库的名字（请提前在数据库中建立）')
#    db = pymysql.connect(host = 'localhost',user = 'root',password = '841658601',port = 3306,db = 'spiders')
    db = pymysql.connect(host = 'localhost',user = user,password = password,port = port,db = db)
    cursor = db.cursor()
    createSqlBase = 'CREATE TABLE IF NOT EXISTS musicsdata(songname VARCHAR(255) NOT NULL,singer VARCHAR(255) NOT NULL,id VARCHAR(255) NOT NULL,PRIMARY KEY (id))'
    cursor.execute(createSqlBase)
    db.commit()

else:
    pass

#构建请求头
headers = {
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'
        }


# In[定义获取页面的函数]

def web_scrath(url,headers = headers,method = 'get',auth = None,cookies = None):
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


# In[定义清理返回的页面的内容函数]
#给函数传递获取后的内容直接返回
    
def web_data_cleaner(web_data):
    
    dataSearch = web_data

    dataStr = dataSearch.text#获取内容

    dataStr = dataStr[9:]#返回的内容需要修正下格式
    dataStr = dataStr[:-1]

#后来我发现转化成json格式更好处理
    dataLoaded = json.loads(dataStr)#转化成json格式

    midVal = dataLoaded['data']['song']['list']#选取所需的列表

    return midVal

# In[定义获取音乐的内容]
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

# In[定义下载音乐的函数]

uin = '84165801'#必须要qq号才能获取guid
guid = '1585847759941'
#keyDownLink = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}'%(guid,guid,songMid,uin,uin)

#传入是获取的songMid列表和第几首歌还有uin和guid

def music_download(songMid,i,uin,guid):
    uin = '84165801'#必须要qq号才能获取guid     ！！！！！！！！11!
    guid = '1585890083908'#登录后的qq音乐网页中的musics.fcg?g_tk中找

#如果是用爬虫来获取这个，要用到session来维持会话

    keyDownLink = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"uin":"%s"}},"comm":{"uin":%s}}'%(guid,guid,songMid,uin,uin)
    keyDownLink = web_scrath(keyDownLink)
    vkeyData = json.loads(keyDownLink.text)

    vkey = vkeyData['req_0']['data']['midurlinfo'][0]['purl']
    if vkey is None:#当选取的音乐是vip音乐时，返回的vkey是一个空的列表
        print('这是vip音乐，无法下载')
        pass
    musicDownLoadLink = 'https://isure.stream.qqmusic.qq.com/%s'%(vkey)
    print(musicDownLoadLink)

    data = web_scrath(musicDownLoadLink)
    #师兄师姐注意更改路径！！！！
    name = r"./musicdownload/{}{}{}.mp3".format(songData[i][1],songData[i][2],songData[i][0])#设置保存的路径和文件名
    
#检查文件命名

    nameCheck = name
    nameCheck = re.match(r'.+([\?\*\"\<\>\|]).+',nameCheck)#检查文件的命名，win系统不允许列表中的字符存在
    
    
    if nameCheck is None:
    
        file = open(name,'wb')
        file.write(data.content)
        file.close()
        print(name+'下载成功')
    else:
        intab = "?*/|><\""
        outtab = "       "
        trantab = str.maketrans(intab, outtab)#建立字符之间的映射（注意长度要相同）
        name = name.translate(trantab)#转换字符
        file = open(name,'wb+')
        file.write(data.content)
        file.close()
        print(name+'下载成功')
# In[定义写入数据库的函数]

#传入songData列表和页码
def write_data_into_database(songData,page):
    for i in range(len(songData)):#按列表中的元素写入
        try:
            insertData = 'INSERT INTO musicsdata(songname,singer,id) VALUES (%s,%s,%s)'
            cursor.execute(insertData,(songData[i][1],songData[i][2],songData[i][0]))
            db.commit()
            print(''+songData[i][1]+''+'数据库写入成功')
        except:#设置错误捕捉
            db.rollback()
            print("歌曲存在,返回")
    
# In[定义主执行函数]
    
def musicLove():
    singerOrSongname = input('输入歌手名或者歌名:')
    page = input('输入查询范围（输入整数）')
    global songData
    songData = []
    global songMidList
    songMidList = []
    download = input('输入是否下载（yes，no）')
    download = re.match('Yes',download,flags= re.I)
    

    for i in range(int(page)):
        i=i+1
        searchUrl = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p={1}&n=10&w={0}'.format(singerOrSongname,i)#可以改页码
        webData = web_scrath(searchUrl)
        webData = web_data_cleaner(webData)
        if webData != []:
            pageCount = (i-1)*10
            get_music_info(webData,pageCount)
        else:
            print('歌曲信息获取完成')
    
    if download is not None:
        for i in range(len(songMidList)):
            music_download(songMidList[i],i,uin,guid)
        if dbConnect == 'yes':
            write_data_into_database(songData,pageCount)
        else:
            pass
    else:
        pass
        
    print('程序执行完毕')
#%%
musicLove()




















