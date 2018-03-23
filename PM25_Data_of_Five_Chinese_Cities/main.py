# -*- coding: utf-8 -*-

"""
Jingyi Lu
    版本:     1.0
    日期:     2018/03
    文件名:    main.py
    功能：     主程序

    实战案例1-1：中国五大城市PM2.5数据分析 (1)
    任务：
        - 五城市污染状态
        - 五城市每个区空气质量的月度差异

    数据集来源：https://www.kaggle.com/uciml/pm25-data-for-five-chinese-cities
"""

import csv
import os
import numpy as np
from PM25_Data_of_Five_Chinese_Cities.config import *

def load_data(data_file, usecols):
    """
        读取数据文件，加载数据
        参数：
            - data_file:    文件路径
            - usecols:      所使用的列
        返回：
            - data_arr:     数据的多维数组表示
    """
    data = []
    with open(data_file, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        # === Step 2. 数据处理 ===
        for row in data_reader:
            # 取出每行数据，组合为一个列表放入数据列表中
            row_data = []
            # 注意csv模块读入的数据全部为字符串类型
            for col in usecols:
                str_val = row[col]

                # 条件表达式的使用
                # 数据类型转换为float，如果是'NA'，则返回nan(便于后续判断)
                row_data.append(float(str_val) if str_val != 'NA' else np.nan)

            # 如果行数据中不包含nan才保存该行记录
            if not any(np.isnan(row_data)):
                data.append(row_data)

    # 将data转换为ndarray
    data_arr = np.array(data)
    return data_arr


def get_polluted_perc(data_arr):
    """
        获取污染占比的小时数
        规则：
            重度污染(heavy)     PM2.5 > 150
            重度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
        参数：
            - data_arr: 数据的多维数组表示
                        由main中的调用者知，data_arr中每行的数据依次为: year, month, PM * 3 (3个不同地域的PM值)
        返回：
            - polluted_perc_list: 污染小时数百分比列表


    """
    # 将每个区的PM值平均后作为该城市小时的PM值
    # 按行取平均值                                # axis=1 表示行/横向(操作数据为每行的数据)
    hour_val = np.mean(data_arr[:, 2:], axis=1) # ':'表示所有行; '2:'表示从第2列~最后(列从0起)(即：3个不同地域的PM值)
    # 总小时个数(一行是数据是每小时的PM2.5值, 故下句统计总共记录PM2.5的小时数)
    n_hours = hour_val.shape[0] # shape[0]: 第一维度x的长度, 即行的总数！  shape[1]: 第二维度y的长度！
    # 重度污染小时个数(一行是数据是每小时的PM2.5值！！！)
    n_heavy_hours = hour_val[hour_val > 150].shape[0]
    # 中度污染小时个数
    n_medium_hours = hour_val[(hour_val > 75) & (hour_val <= 150)].shape[0]
    # 轻度污染小时的个数
    n_light_hours = hour_val[(hour_val > 35) & (hour_val <= 75)].shape[0]
    # 优良空气小时的个数
    n_good_hours = hour_val[hour_val <= 35].shape[0]
    # 得到某地区x度污染/优良空气(小时数)的占比
    polluted_perc_list = [n_heavy_hours / n_hours, n_medium_hours / n_hours,
                          n_light_hours / n_hours, n_good_hours / n_hours]
    return polluted_perc_list


def get_avg_pm_per_month(data_arr):
    """
        获取每个区每月的平均PM值
        参数：
            - data_arr: 数据的多维数组表示
                        由main中的调用者知，data_arr中每行的数据依次为: year, month, PM * 3 (3个不同地域的PM值)
        返回：
            - results_arr:  多维数组结果
    """
    results = []

    # 获取年份 mnp.unique():获取不重复的数据
    years = np.unique(data_arr[:, 0]) # [:, 0]表示提取data_arr中所有行,第0列数据('year')
    for year in years:

        # NumPy中的条件索引
        # 获取当前遍历年份year的所有数据
        # data_arr[:, 0] == year 表示判断data_arr中的第0列中的数据是否等于year，如果是返回True，否则为False，即布尔值数组
        # 然后将上述结果作为mask作用于原始数组data_arr中，过滤出符合条件的数据
        year_data_arr = data_arr[data_arr[:, 0] == year] # bool数组，类似于"图层蒙板"。获取data_arr中所有符合要求的数据(不仅仅是year，还有year对应的一系列数据)

        # 获取数据的月份
        month_list = np.unique(year_data_arr[:, 1]) # unique获得符合要求的数据相应的月份(不重复)（因为选中的数据中肯定有重复的月份,即第1列数据(从0起)。故用unique去重）
        for month in month_list:
            # 获取符合要求的月份的所有数据               # [:, 1]表示遍历范围：所有行,第1列(从0起)
            month_data_arr = year_data_arr[year_data_arr[:, 1] == month] # bool数组。获取year_data_arr中所有符合要求的数据(不仅仅是month，还有month对应的一系列数据)
            # 计算当前月份PM的均值（np.mean()）
            mean_vals = np.mean(month_data_arr[:, 2:], axis=0).tolist()

            # 格式化字符串
            row_data = ['{:.0f}-{:02.0f}'.format(year, month)] + mean_vals
            results.append(row_data)

    results_arr = np.array(results)
    return results_arr


def save_stats_to_csv(results_arr, save_file, headers):
    """
        将统计结果保存至csv文件中
        参数：
            - results_arr:   多维数组结果
            - save_file:    文件保存路径
            - headers:      csv表头
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in results_arr.tolist():
            writer.writerow(row)


def main01():
    """
        主函数
    """
    polluted_state_list = []


    for city_name, (filename, cols) in data_config_dict.items():
        # === Step 1+2. 数据获取 + 数据处理 ===
        data_file = os.path.join(dataset_path, filename)   # common_cols有year, month

        # 列表推导式的使用
        # ['PM_' + col for col in cols]是将字符串'PM_'和区的名称进行拼接，返回以'PM_'开头的字符串list
        # list相加，返回需要使用的列
        usecols = common_cols + ['PM_' + col for col in cols] # 说明只提取每行数据中的 year, month, config中的字典中的各个cols
        data_arr = load_data(data_file, usecols)

        print('{}共有{}行有效数据'.format(city_name, data_arr.shape[0]))
        # 预览前10行数据
        print('{}的前10行数据：'.format(city_name))
        print(data_arr[:10])

        # === Step 3. 数据分析 ===
        # 五城市污染状态，统计污染小时数的占比
        polluted_perc_list = get_polluted_perc(data_arr)
        polluted_state_list.append([city_name] + polluted_perc_list)
        print('{}的污染小时数百分比{}'.format(city_name, polluted_perc_list))

        # 五城市每个区空气质量的月度差异，分析计算每个月，每个区的平均PM值
        results_arr = get_avg_pm_per_month(data_arr)
        print('{}的每月平均PM值预览：'.format(city_name))
        print(results_arr[:10])

        # === Step 4. 结果展示 ===
        # 4.1 保存月度统计结果至csv文件
        save_filename = city_name + '_month_stats.csv'
        save_file = os.path.join(output_path, save_filename)
        save_stats_to_csv(results_arr, save_file, headers=['month'] + cols)
        print('月度统计结果已保存至{}'.format(save_file))
        print()

    # 4.2 污染状态结果保存
    save_file = os.path.join(output_path, 'polluted_percentage.csv')
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['city', 'heavy', 'medium', 'light', 'good']) # 写在同一行
        for row in polluted_state_list:
            writer.writerow(row)
    print('污染状态结果已保存至{}'.format(save_file))


if __name__ == '__main01__':
    main01()
