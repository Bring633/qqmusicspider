# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:42:58 2020

@author: MSI-NB
"""

import pandas as pd 
#In[找到两个id之间的相似度]


def finding_similarity(df1,df2):#输入为某个serie
    
    dataBool = df1.notnull() & df2.notnull()
    dataBool = dataBool.value_counts(dropna = False)
    try:
        num = dataBool.loc[True]
        likeNum = df1.value_counts().loc[1.0] * df2.value_counts().loc[1.0]
        similarity = num/pow(likeNum,0.5)
        return similarity
    except:
        #print("there isn't similarity between two series")此时两列没有相似的元素
        pass
    
#In[找到一个在table中id与剩余的id的相似度]

def finding_sim_with_otherid(df,baseid,num):#num是范围
    
    global dict1
    dict1 = {}
    global listBaseid
    listBaseid = []
    
    df1=df[baseid]#选择对应的col
    
    for i in df.columns[:num]:#找出用户A和其它用户的相似度
       df2 = df[i]
       similarity = finding_similarity(df1,df2)
       
       if similarity != None:
           dict1[i] = similarity
       else:
           pass
       
    listBaseid = list(df[df[baseid].notnull()].index)#找出用户的喜欢的歌手，并转换成列表
    
    #对dict的值进行排序
    dict1 = dict(sorted(dict1.items(),key = lambda x:x[1],reverse = True))#dict.items是返回keys and values 的元组，x相当于取出iterable object(第一个parameter)，key是用来比较的依据
    try:
        del(dict1[baseid])
    except:
        pass
    
#In[返回推荐]

def recommandations(df,dict1,listBaseid):#输入先前确定的相关最高的字典
    global recommandation
    recommandation = []
    
    for keys in dict1:
        if dict1[keys] >= 0.35:#设置一个相关度阈值，如果另一个用户的相关度大于0.5
            
            a = list(df[keys][df[keys].notnull()].index)#找出另一个用户喜欢的歌
            for j in a:#在alist中不重复添加
                if j not in recommandation:
                    if j not in listBaseid:
                        recommandation.append(j)
                    else:
                        pass
                else:
                    pass
        else:
            pass
    print('为您推荐'+recommandation)
    if list(dict1.values())[0] <0.35:
        print('您喜欢的歌手较为小众，暂无推荐')
    return recommandation

#In[整合函数]
    
def song_recommandations(df,id,num=2000):
    global recommandation
    print('Processing')
    finding_sim_with_otherid(df,id,num)
    recommandation = recommandations(df,dict1,id)
    print('Completed')

def readData():
    data = pd.read_csv(r'./dataForTrain.csv',encoding = 'utf8',index_col = 'singer')
    try:
        data.drop(['Unnamed: 0'],axis =1,inplace = True)
    except Exception as e:
        pass
    data['likesinger'] =1
    return data

def readinput(data):
    
    singer = []
    
    single_singer = input("please input singer's name(q denotes for ending)")
    
    while single_singer!='q':
        singer.append(single_singer)
        single_singer = input("please input singer's name(q denotes for ending)")

    df = pd.DataFrame(index = data.index,columns = ['user'])

    for i in singer:
        try:
            data.loc[i,:]
            df.loc[i,'user'] = 1
        except Exception as e:
            print("该歌手未收录,推荐失败")
            return None,1
    
    return pd.concat([df,data],axis = 1),0
        

def main():
    
    data = readData()
    data_with_input,flags = readinput(data)
    if flags ==0:
        song_recommandations(data_with_input,'user')
    else:
        pass
    
if __name__ == '__main__':
    main()

"""
data = pd.read_csv(r'./dataForTrain.csv',encoding = 'utf8',index_col = 'singer')
dataForTest = pd.read_csv(r'./dataForTest.csv',encoding = 'utf8',index_col = 'singer')
try:
    data.drop(['Unnamed: 0'],axis =1,inplace = True)
except Exception as e:
    pass
data['likesinger'] =1
#建立一个table index 是用户 columns是singer

#对数据的要求，数据需要转成DataFrame的形式，并且以用户为index，columns是所有用户喜欢的singer，values是用户对singer是否喜欢，1为喜欢，0为不喜欢

# In[评价函数]

    
global id
id = '001a11b6b9a82c4bec0b1e1e472067a8d14feab7'
#计算单个用户的评价值
def Evaluations(dftest,id,recommandationList):
    
    if id not in dftest.columns:
        print('该用户没有被划分入数据集')
        return 0
    else:
        
        targetRow = dftest[id][dftest[id].notnull()]
        targetList = list(targetRow.index)
    
    #计算分子
        num1 = 0
        for i in recommandationList:
            if i in targetList:
                num1+=1
            else:
                pass
    
    try:
        precision = num1/len(recommandationList)
        recall = num1/len(targetList)
    except:
        return 0,0
    
    return precision,recall

#In[Create dataset and find PRECISION,RECALL and CONVERAGE]
    
listPre = []
listRecal =[]
userid = []
recommandLen = 0

for i in dataForTest.columns[:20]:
    song_recommandations(data,i)
    precision,recall = Evaluations(dataForTest,id = i,recommandationList = recommandation)
    listPre.append(precision)
    listRecal.append(recall)
    userid.append(i)
    recommandLen =+len(recommandation)#计算推荐了多少歌

dataSet = pd.DataFrame({"Precision":listPre,"Recall":listRecal},index = userid)
    
PRECISION = dataSet['Precision'].mean()
RECALL = dataSet['Recall'].mean()
COVERAGE = recommandLen/len(data.index)
    
"""  
    
    
    
    
    
    
    
    
    
    
    
    