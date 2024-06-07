# @File  : switchLabels.py
# @Author: horsefly
# @Time: 2024/6/5 下午7:48 
# -*- coding: utf-8 -*-

import os

def switch_strs2lists(image, labels):
    '''
    将字符串列表的标签转化为列表，列表中的每个元素为四个坐标，单位为原图像素坐标下的一个像素
    :param image:图像
    :param labels:标签的字符串列表（每一串字符串末尾没有换行符）
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


def switch_xywh2xyxyxyxy(label_files):
    '''
    将标签文件中xywh格式的标签转化为四点格式，从左上角点开始逆时针
    :param label_files:标签文件的绝对路径列表
    :return:none
    '''

    # 读取并转换标签
    for label_file in label_files:
        new_labels = []
        with open(label_file, "r") as file:
            for line in file:
                boys = line.split(" ")
                # 删掉换行符
                boys[4] = boys[4][:-2]
                x1 = float(boys[1]) - float(boys[3]) / 2
                y1 = float(boys[2]) - float(boys[4]) / 2
                x2 = float(boys[1]) - float(boys[3]) / 2
                y2 = float(boys[2]) + float(boys[4]) / 2
                x3 = float(boys[1]) + float(boys[3]) / 2
                y3 = float(boys[2]) + float(boys[4]) / 2
                x4 = float(boys[1]) + float(boys[3]) / 2
                y4 = float(boys[2]) - float(boys[4]) / 2

                newboy = boys[0] + " " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(
                         y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4)
                new_labels.append(newboy)

        # 写入原文件
        with open(label_file, "w") as file:
            for l in new_labels:
                file.write(l)



