# @File  : switchLabels.py
# @Author: horsefly
# @Time: 2024/6/5 下午7:48 
# -*- coding: utf-8 -*-

import os

def switch_strs2lists(image, labels):
    '''
    将字符串列表的标签转化为列表，列表中的每个元素为四个坐标，单位为原图像素坐标下的一个像素
    :param image:图像
    :param labels:标签的字符串列表
    :return:标签的坐标列表列表
    '''

    # 获取图像宽高
    height, width, _ = image.shape

    newlabels = []
    for label in labels:
        boys = label.split(" ")
        for i in range(len(boys)):
            boys[i] = float(boys[i])

        # 将坐标化为绝对坐标
        xyxyxyxy = list(map(lambda x, y: x * y, boys[1:], [width, height, width, height, width, height, width, height]))

        p1 = list(map(int, xyxyxyxy[0: 2]))
        p2 = list(map(int, xyxyxyxy[2: 4]))
        p3 = list(map(int, xyxyxyxy[4: 6]))
        p4 = list(map(int, xyxyxyxy[6: 8]))

        newlabels.append(p1 + p2 + p3 + p4)

    return newlabels
