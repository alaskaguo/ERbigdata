# -*- coding: utf-8 -*-
"""
Created on Sun May 13 20:28:15 2018

@author: 郭峰医生
"""
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as  plt
import numpy as np
def combinefiles(file1,file2,file3,file4):
    '''combine four xlsx files to one'''
    #load data
    data1 = pd.read_excel(file1)
    data2 = pd.read_excel(file2)
    data3 = pd.read_excel(file3)
    data4 = pd.read_excel(file4)
    #combine data
    data_nh = pd.concat([data1,data2])
    data_hx = pd.concat([data3,data4])
    data_total = pd.concat([data_nh,data_hx])
    return data_total;
def outpatientcounts(data_total):
    #load the rec_date column
    date_rec_group=data_total.rec_date
    #count values in the column and sort index
    datecounts = date_rec_group.value_counts().sort_index()
    #return a series
    return datecounts;
def dia_count(data_total,simptom_list):
    simptom_count_list = []
    for simptom_re,simptom in simptom_list.items():
        simptom_counts = data_total['diagnosis'].str.contains(simptom,na = False).sum()   
        simptom_count_list.append(simptom_counts)
    simptom_df = pd.DataFrame({'诊断':list(simptom_list.keys()),
                               '病例数':simptom_count_list})
    ratio_list = []
    for number in simptom_count_list:
        ratio = str('{:.2f}'.format(number*1000/simptom_df['病例数'].sum())+'‰')
        ratio_list.append(ratio)
    simptom_df['构成比'] = ratio_list
    simptom_df = simptom_df.sort_values(by = '病例数',ascending = False)
    return simptom_df     
def combinedata(files):
    '''load and combine files in files list'''
    file = []
    for f in files:
        file_df = pd.read_csv(f,header = None,names = ['dp','doc_nm','pat_nm','pat_id',
                                              'rec_date','rec_time','diagnosis'])
        file.append(file_df)
    data_total = pd.concat(file)
    return data_total;

def barh_creator(dia_count_df):
    plt.rcdefaults()
    plt.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False 
    fig,ax =plt.subplots(figsize = (8,6),dpi = 300,edgecolor = 'white')    #   ax为子图
    fontdics = {'title':{'family': 'KaiTi',
                'style': 'normal',
                'weight': 'normal',
                'color':  'black', 
                'size': 14},
                'number':{
                'family': 'Times New Roman',
                'style': 'normal',
                'weight': 'normal',
                'color':  'black', 
                'size': 10}}  #字体字典
    amount = dia_count_df['病例数'] #   生成病历数列表
    ylabel =list(dia_count_df['诊断']) 
    ratio_list = dia_count_df['构成比']
    y_pos =np.arange(len(ylabel)) #   根据人数生成的数据组y_post
        #  生成横条图
    ax.barh(y_pos,amount,align='center',color='green',ecolor='black')       
    ax.set_yticks(y_pos)   #   设置纵坐标的刻度
    ax.set_yticklabels(ylabel) #   设置纵坐标的标签(诊断名)
    ax.invert_yaxis()  #   把Y反转,取消这一行运行一下就明白了
    ax.set_xlabel('病历数')   #   显示X轴标签
    for x, y,r in zip(y_pos,amount,ratio_list):
        plt.text(y , x , r,fontdict = fontdics['number'],verticalalignment='center')
    plt.show()    
    return fig;#  显示图片  
