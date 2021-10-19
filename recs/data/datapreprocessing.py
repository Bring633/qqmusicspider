# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 01:04:07 2020

@author: MSI-NB
"""
import random
import pandas as pd
import re

f = open(r'C:\Users\MSI-NB\Desktop\研发\recs\data\music_data.txt',encoding = 'utf8')
data = f.read()

#%%
pattern = r'(.+),(.+)'
dataList = re.findall(pattern,data)
def separating_data(dataList,size):#size划分多少个数据集
    global testData
    global trainData
    testData =[]
    trainData =[]
    k = random.randint(0,size)
    
    for i in dataList:
        
        if random.randint(0,size) == k:
            testData.append(i)
        else:
            trainData.append(i)
#%%
separating_data(dataList,8)
#%%
def build_df(listToBuild):
    
    listid = []
    listsinger = []
    
    for i in listToBuild:
        listid.append(i[0])
        listsinger.append(i[1])
        
    data = {'userid':listid,
            'singer':listsinger}

    dataset = pd.DataFrame(data)

    return dataset

#%%
    
dataForTrain = build_df(trainData)
dataForTest = build_df(testData)

#%%
def data_change_format(df):
#    df.drop(['Unnamed: 0'],axis =1,inplace = True)
    df['likesinger'] =1

#建立一个table index 是用户 columns是singer
    df = pd.pivot_table(df,index = 'singer',columns = 'userid',values = 'likesinger')#index直接传入名字就好
    
    return df

#%%
dataForTrain = data_change_format(dataForTrain)
dataForTest = data_change_format(dataForTest)
#%%

dataForTrain.to_csv(r'C:\Users\MSI-NB\Desktop\研发\data\dataForTrain1.csv')
dataForTest.to_csv(r'C:\Users\MSI-NB\Desktop\研发\data\dataForTest1.csv')

#%%
f.close()
