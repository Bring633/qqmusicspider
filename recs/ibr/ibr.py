# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:50:20 2020

@author: MSI-NB
"""
import numpy as np
import pandas as pd
import random
import json


#In[define variable]
global simDict
simDict = {}
global simListLow
simListLow =[]
#In[finding similarity]

def finding_sim(df,singer,num = 2000):
    if singer not in simListLow:
        simDict1 = {}
        confirmDict = {}
    
        for i in df.columns[:num]:
            filterCols = df[singer].notnull() & df[i].notnull()#找到同时喜欢两首歌的id
        
            numBoth = df[singer].loc[filterCols].sum()#找出分子
        
            #找出分母
            num1 = df[singer].loc[df[singer]==1].sum()
            num2 = df[i].loc[df[i]==1].sum()
        
            #计算相关度
            similarity = numBoth/pow(num1*num2,0.5)
            if i != singer and similarity >=0.25 :
                simDict1[i] = similarity
                confirmDict[i] = 1
            else:
                confirmDict[i] = 0
                pass
    
    #写入global value
        if simDict1 !={}:
            simDict[singer] = dict(sorted(simDict1.items(),reverse = True,key = lambda x:x[1])[:5])
        else:
            simListLow.append(singer)
    else:
        pass
    
#In[recommandations]

global id


def Recommandations(df,id = id):
    
    global recommandList
    #找出目标用户喜欢的歌，并据此找出用户喜欢的歌和其他歌的相关度
    objectRow = df.loc[id,:]
    objectRow.dropna(inplace = True)
    objectList = dict(objectRow)
    
    recommandList = {}

    #写入recommandlist，在写入前判断之前有没有找过相关度，有的跳过
    for i in objectList:
        if i not in simDict and i not in simListLow:
            finding_sim(df,i)
        if i in simDict:
            recommandList[i] = simDict[i]
        elif i in simListLow:
            print(i+'在训练样本中过于稀少,故不予推荐')

            
    #从推荐的列表中随机抽取歌手来推荐
    num = []
    if len(recommandList)>=5:
        while(len(num)<5):
            num1 = random.randint(0,len(recommandList)-1)
            
            if num1 not in num:
                num.append(num1)
            
            else:
                continue
    else:
        for i in range(0,len(recommandList)):
            num.append(i)
    
    recommandList = list(recommandList.items())
    
    for i in num:
        recommandSingerList = list(recommandList[i][1].keys())
        print("根据您喜欢{0}，为您推荐{1}".format(recommandList[i][0],recommandSingerList))
    
#In[evaluations]
        
def Evaluations(dataTest,id = id):
    
    if id not in dataTest.columns:
        print('此用户没有被划分到测试集中')
        return 0,0
    else:
        #找出测试集中用户喜欢的歌
        dataFilter = dataTest[id].notnull()
        targetCol = dataTest[id][dataFilter]
        targetList = list(targetCol.index)

        listRec = []
    
    #从recommandList中写不重复的歌手到ListRec中
        for i in recommandList:
            for j in i[1]:
                if j not in listRec:
                    listRec.append(j)
    #计算分子
        num1 = 0
        for i in listRec:
            if i in targetList:
                num1 =+1
            else:
                pass
            
    #计算单用户的precision值和recall值
        if len(listRec) != 0:
            Precision = num1/len(listRec)
            Recall = num1/len(targetList)
        else:
            return np.nan,np.nan
            #return 0,0 分母为零，即没有推荐，所以不该算入推荐故使用nan值而不是0值
        
        
        return Precision,Recall


#2021.10.19新增

def read_simDict():
    #simDictLow
    file2 = open(r'./similarityLow.txt','r+',encoding = 'utf8')

    list1 = file2.readlines()#读完一次后，文件指针会放到文件的末尾，再次读取为空
    list2 = []#即是simdictlow

    for i in list1:
        i = i.strip()#注意要加i=
        list2.append(i)

    #simDict

    file1 = open(r'./similarity.txt','r+',encoding = 'utf8')

    dict1=file1.readlines()
    dict1 = json.loads(dict1[0])
    global simDict
    simDict = dict(dict1)
    
    return None

def readinput():
    
    singer = []
    
    single_singer = input("please input singer's name(q denotes for ending)")
    
    while single_singer!='q':
        singer.append(single_singer)
        single_singer = input("please input singer's name(q denotes for ending)")

    return pd.DataFrame(columns = singer,index = [0]).fillna(1)
        
        
    
def main():
    
    read_simDict()
    like_singer = readinput()
    Recommandations(like_singer,0)
    
if __name__=='__main__':
    
    main()
    
    



"""
# In[read data in]

data = pd.read_csv(r'./dataForTrain1.csv',encoding = 'utf8')

data.drop('Unnamed: 0',axis = 1,inplace = True)
data['likes'] = 1

dataForTest = pd.read_csv(r'./dataForTest1.csv',encoding = 'utf8')
dataForTest['likes'] = 1

#对数据的要求，数据需要转成DataFrame的形式并且以用户为index，columns是所有用户喜欢的singer，values是用户对singer是否喜欢，1为喜欢，0为不喜欢
#In[Transform data]

dataTrans = pd.pivot_table(data,index = 'userid',columns = 'singer',values = 'likes')#以userid为index，singer为columns
dataForTest = pd.pivot_table(dataForTest,columns = 'userid',index = 'singer',values = 'likes')

#In[caculate evaluations]
global evaDict#创立全局变量，储存precision，recall值
evaDict = {}

count =0 
for i in dataTrans.index[:2000]:#计算前20个用户的precison和recall值
    id = i
    Recommandations(dataTrans,id = id)
    Precision,Recall = Evaluations(dataForTest,id =id)   
    print(count)
    count+=1
    evaDict[id] = Precision,Recall#赋予变量值
#
id=[]
precision=[]
recall = []

for i in evaDict.keys():
    id.append(i)
    precision.append(evaDict[i][0])
    recall.append(evaDict[i][1])

#In[创建一个Dataframe来计算值]
    
eva = pd.DataFrame({'Precision':precision,'Recall':recall},index = id)
eva = eva.replace(0,value = np.nan).dropna()

PRECISION = eva["Precision"].mean()
RECALL = eva['Recall'].mean()
COVERAGE = len(simDict)/len(dataTrans.columns)

"""
#In[输出歌的相似度]
"""
file1 = open(r'./similarity.txt','w+',encoding = 'utf8')
file2 = open(r'./similarityLow.txt','w+',encoding = 'utf8')

#file1
sim = json.dumps(simDict)#转换成json格式
file1.write(sim)

#file2
for i in simListLow:
    file2.write(i)
    file2.write('\n')

file1.close()
file2.close()

# In[读取文件并转化成list]# In[读取文件并转化为dict]

#simDictLow
file2 = open(r'./similarityLow.txt','r+',encoding = 'utf8')

list1 = file2.readlines()#读完一次后，文件指针会放到文件的末尾，再次读取为空
list2 = []#即是simdictlow

for i in list1:
    i = i.strip()#注意要加i=
    list2.append(i)

#simDict

file1 = open(r'./similarity.txt','r+',encoding = 'utf8')

dict1=file1.readlines()
dict1 = json.loads(dict1[0])
simDict = dict(dict1)
"""
