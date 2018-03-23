# -*- coding: utf-8 -*-

"""
    作者:     Jingyi Lu
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件


    案例描述
随着PM2.5污染的严重性被越来越多地认识，PM2.5数据的质量也成为人们关心的话题。目前，公众判断所在城市
PM2.5污染程度最常用的两大数据源，一是美国驻华大使馆（或领事馆）所发布的数据，二是中国环保部的实时播
报。然而，中国环保部所发布的数据真实性却不时遭到质疑，例如《华尔街日报》就曾在2012年的一篇报道中
称：北京官方的PM2.5数据与美国大使馆的数据不一致！也有不少学者著文，研究探讨中国空气污染数据的人为干
扰。一些公众也持怀疑态度，认为环保部门“美化”数据的讨论不绝于耳。
数据可靠性是研究的基石，如果没有高质量的数据真实反映一个城市大气的污染程度，大气污染防治就无从谈起。
该案例选取北京、上海、广州、成都、沈阳五个城市美国使/领馆及其邻近的环保部站点在2013-2015三年间的
PM2.5数据，运用统计学方法验证美国使/领馆和邻近的环保部站点数据的可靠性



    任务描述
统计每个城市每天的平均PM2.5的数值
基于天数对比中国环保部和美国驻华大使馆统计的污染状态
"""

import os

# 指定数据集路径
dataset_path = './data'

# 结果保存路径
output_path2 = './output2'
if not os.path.exists(output_path2):
    os.makedirs(output_path2)

common_cols2 = ['year', 'month', 'day', 'PM_US Post']

# 每个城市对应的文件名及所需分析的列名
# 以字典形式保存，如：{城市：(文件名, 列名)}
data_config_dict = {'beijing': ('BeijingPM20100101_20151231.csv',
                                ['Dongsi', 'Dongsihuan', 'Nongzhanguan']),
                    'chengdu': ('ChengduPM20100101_20151231.csv',
                                ['Caotangsi', 'Shahepu']),
                    'guangzhou': ('GuangzhouPM20100101_20151231.csv',
                                  ['City Station', '5th Middle School']),
                    'shanghai': ('ShanghaiPM20100101_20151231.csv',
                                 ['Jingan', 'Xuhui']),
                    'shenyang': ('ShenyangPM20100101_20151231.csv',
                                 ['Taiyuanjie', 'Xiaoheyan'])
                    }
