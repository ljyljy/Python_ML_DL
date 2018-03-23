# -*- coding: utf-8 -*-

"""
Jingyi Lu
    版本:     1.0
    日期:     2018/03
    文件名:    config.py
    功能：     配置文件
"""
import os

# 指定数据集路径
dataset_path = './data'

# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 公共列 为后续输出结果的第一列format
common_cols = ['year', 'month']
common_cols2 = ['year', 'month', 'day','PM_US Post']



# config.data_config_dict 为提前构造的字典数据
# key为城市拼音
# value为tuple，其中tuple中第一个元素为文件名，第二个元素为该城市对应的区名称列表
# 如: 北京
# key为 'beijing'
# value为 ('BeijingPM20100101_20151231.csv', ['Dongsi', 'Dongsihuan', 'Nongzhanguan'])
# 遍历字典时，可以通过以下方法同时取出城市拼音、文件名及对应的区名称列表
# for city_name, (filename, cols) in config.data_config_dict.items():
#    ...

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
