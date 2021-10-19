# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:31:00 2020

@author: MSI-NB
"""

import pymysql

#初始化数据库
#本地数据库，user名是root，用的是spiders数据库，3306端口
user = input('请输入数据库用户名')
password = input('请输入数据库用户的密码')
port = int(input('请输入端口'))
db = input('请输入数据库的名字（请提前在数据库中建立）')

#root,,3306,spiders

db = pymysql.connect(host = 'localhost',user = user,password = password,port = port,db = db)
cursor = db.cursor()
createSqlBase = 'CREATE TABLE IF NOT EXISTS musicsdata(songname VARCHAR(255) NOT NULL,singer VARCHAR(255) NOT NULL,id VARCHAR(255) NOT NULL,PRIMARY KEY (id))'
cursor.execute(createSqlBase)
db.commit()

# [定义写入数据库的函数]

#传入songData列表和页码
def write_data_into_database(songData,page):
    for i in range(len(songData)):#按列表中的元素写入
        try:
            insertData = 'INSERT INTO musicsdata(songname,singer,id) VALUES (%s,%s,%s)'
            cursor.execute(insertData,(songData[i][1],songData[i][2],songData[i][0]))
            db.commit()#提交数据到数据库中
            print(''+songData[i][1]+''+'数据库写入成功')
        except:#设置错误捕捉
            db.rollback()
            print("歌曲存在,返回")
    