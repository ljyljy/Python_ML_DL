# -*- coding: utf-8 -*-

"""
    作者:     Jingyi Lu
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    实战案例1-2：中国五大城市PM2.5数据分析 (2)
    任务：
        - 统计每个城市每天的平均PM2.5的数值
        - 基于天数对比中国环保部和美国驻华大使馆统计的污染状态

    数据集来源：https://www.kaggle.com/uciml/pm25-data-for-five-chinese-cities

"""

import os
import pandas as pd
import numpy as np

import PM25_Data_of_Five_Chinese_Cities2.config as config

def get_china_us_pm_df(data_df, suburb_cols):
    """
        处理获取中国与美国统计的PM数据
        参数：
            - data_df:      包含城市PM值的DataFrame
            - suburb_cols:  城市对应区的列名
        返回：
            - proc_data_df:   处理后的DataFrame
    """
    pm_suburb_cols = ['PM_' + col for col in suburb_cols]

    # 取(新增一列)PM的均值为中国环保部在该城市的测量值
    # 按行计算——每一行(每一天)都有一个对应的PM_China(均值)
    data_df['PM_China'] = data_df[pm_suburb_cols].mean(axis=1)

    # 取出有用的列构建新的DataFrame               ❤️注意此处有中括号'[]'!
    proc_data_df = data_df[config.common_cols2 + ['city', 'PM_China']]

    # 数据预览
    print('处理后的数据预览：')
    print(proc_data_df.head())
    return proc_data_df

def preprocess_data(data_df, city_name):
    """
        预处理数据集
        参数：
            - data_df:      数据DataFrame
            - city_name:    城市名
        返回：
            - cln_data_df:  预处理后的数据集
    """
    # 数据清洗，去掉存在空值的行
    cln_data_df = data_df.dropna()

    # 重新构建索引 ❤️常与上句一起使用
    cln_data_df = cln_data_df.reset_index(drop=True)

    # 添加新的一列作为城市名
    cln_data_df['city'] = city_name

    # 输出信息
    print('{}共有{}行数据, 其中有效数据为{}行'.format(city_name, data_df.shape[0], cln_data_df.shape[0]))
    print('{}的前10行有效数据：'.format(city_name))
    print(cln_data_df.head())

    return cln_data_df

def add_date_col_to_df(data_df):
    """
            预处理数据集
            参数：
                - data_df:  数据DataFrame
            返回：
                - proc_data_df:  处理后的数据集
        """
    # DataFrame操作会对原数据产生影响，故copy()
    proc_data_df = data_df.copy()

    # 将'year', 'month', 'day'合并成字符串列'date'(首先 需要现将其转化成str!!! - astype)
    # 转换数据类型 ❤️注意有2层'[[Xxx]]'->内层起到 并列多个数据 的作用(数据类型不同)
    # 说明['year', 'month', 'day']是子DataFrame类型（用两个中括号）
    proc_data_df[['year', 'month', 'day']] = proc_data_df[['year', 'month', 'day']].astype('str')

    # 合并列 ❤️字符串处理 拼接str.cat
    # proc_data_df['data'] = proc_data_df['year'].str.cat([proc_data_df['month'], proc_data_df['day']], sep='-')
    proc_data_df['date'] = proc_data_df['year'].str.cat([proc_data_df['month'], proc_data_df['day']], sep='-')

    # 去除列 #横向删除!!!注意是横向的每一行!!!
    # ❤️❤️删除某些列️->每一行的对应项横向删除；️删除某些行->每一行的对应项纵向删除(如删除多行索引index，则需要删除每一列的纵向对应索引)
    proc_data_df = proc_data_df.drop(['year', 'month', 'day'], axis=1)

    # 调整列的顺序  ❤️注意有2层'[[Xxx]]'-》=>内层起到 并列多个数据 的作用（数据类型不同）
    # data_df['A']的类型是Series，data_df[['A']]的类型是DataFrame
    proc_data_df = proc_data_df[['date', 'city', 'PM_China', 'PM_US Post']]

    return proc_data_df


def add_polluted_state_col_to_df(day_stats):
    """
        根据每天的PM值，添加相关的污染状态
        参数：
            - day_stats:  数据DataFrame
        返回：
            - proc_day_stats: 处理后的数据集
    """

    proc_day_stats = day_stats.copy()

    #分箱
    # -np.inf 负无穷
    bins = [-np.inf, 35, 75, 150, np.inf]
    state_labels = ['good', 'light', 'medium', 'heavy']

    #分箱后，增加新列
    proc_day_stats['Polluted State CH'] = pd.cut(proc_day_stats['PM_China'], bins=bins, labels=state_labels)
    proc_day_stats['Polluted State US'] = pd.cut(proc_day_stats['PM_US Post'], bins=bins, labels=state_labels)

    return proc_day_stats


# pandas.Series.value_counts❤️ 基于'分箱'操作
# Series.value_counts(normalize=False, sort=True, ascending=False, bins=None, dropna=True)
#
# 功能：返回包含唯一值计数的对象。结果对象将按降序排列，以便第一个元素是最常出现的元素。 不包括默认的NA值。
#
# 参数：normalize : boolean, default False             如果为True，则返回的对象将包含唯一值的相对频率。
#
# 　　　sort : boolean, default True             按值排序
#
# 　　　ascending : boolean, default False        按升序排序
#
# 　　　bins : integer, optional    而不是数值计算，把它们分成半开放的箱子，一个方便的pd.cut，只适用于数字数据
#
# 　　　dropna : boolean, default True          不包括NaN的数量。
#
# 返回：计数：Serise
def compare_state_by_day(day_stats):
    """
        基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    """
    city_names = config.data_config_dict.keys()
    city_comparison_list = []
    for city_name in city_names:
        # 找出city_name的相关数据
        city_df = day_stats[day_stats['city'] == city_name]

        # 统计类别个数
        city_polluted_days_count_ch = pd.value_counts(city_df['Polluted State CH']).to_frame(name=city_name + '_CH')
        city_polluted_days_count_us = pd.value_counts(city_df['Polluted State US']).to_frame(name=city_name + '_US')

        city_comparison_list.append(city_polluted_days_count_ch)
        city_comparison_list.append(city_polluted_days_count_us)

    # 横向组合DataFrame
    comparison_result = pd.concat(city_comparison_list, axis=1)
    return comparison_result


def main():
    city_data_list = []

    for city_name, (filename, suburb_cols) in config.data_config_dict.items():
        # === Step 1. 数据获取 ===
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols2 + ['PM_' + col for col in suburb_cols]

        # 读入数据
        data_df = pd.read_csv(data_file, usecols=usecols)

        # === Step 2. 数据处理 ===
        # 数据预处理（dropna()等） ❤简化csv.DictReader()
        cln_data_df = preprocess_data(data_df, city_name)

        # 处理获取中国与美国统计的PM数据
        proc_data_df = get_china_us_pm_df(cln_data_df, suburb_cols)
        city_data_list.append(proc_data_df) # ❤️每一个循环中生成的DataFrame都可以加入到list！！！

        print()

    # 合并5个城市的处理后的数据
    all_data_df = pd.concat(city_data_list) # ❤️循环结束后，list可以拼接到DataFrame！！！

    # 将'year', 'month', 'day'合并成字符串列'date'
    all_data_df = add_date_col_to_df(all_data_df)

    # === Step 3. 数据分析 ===
    # 通过分组操作获取每个城市每天的PM均值
    # 统计每个城市每天的平均PM2.5的数值
    # ❤️多级groupby(类似层级索引): 先按city分组，再按date分组；分组完成后，再取得'PM_China', 'PM_US Post'这两列的均值
    # ❤️注意两个'[[]]':内层'[]'起到 多条数据并列 的作用，（数据类型不同）
    # 说明[['PM_China', 'PM_US Post']]是子DataFrame类型      ❤️
    day_stats = all_data_df.groupby(['city', 'date'])[['PM_China', 'PM_US Post']].mean()

    # 分组操作后day_stats的索引为层级索引['city', 'date']，
    # 为方便后续分析，将层级索引转换为普通列
    # (×) day_stats = day_stats.reset_index(inplace=True) ×
    # (↑)❤️用了inplace=True，就没有返回值了，不可以再用自身去接收
    day_stats.reset_index(inplace=True)


    # 根据每天的PM值，添加相关的污染状态
    day_stats = add_polluted_state_col_to_df(day_stats)

    # 基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    comparison_result = compare_state_by_day(day_stats)

    #  === Step 4. 结果展示 ===
    all_data_df.to_csv(os.path.join(config.output_path2, 'all_cities_pm.csv'), index=False)
    day_stats.to_csv(os.path.join(config.output_path2, 'day_stats.csv'))
    comparison_result.to_csv(os.path.join(config.output_path2, 'comparison_result.csv'))



if __name__ == '__main__':
    main()