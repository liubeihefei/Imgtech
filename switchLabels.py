# @File  : switchLabels.py
# @Author: horsefly
# @Time: 2024/6/5 下午7:48 
# -*- coding: utf-8 -*-

import os


def switch_strs2lists(labels):
    """
    将字符串列表的标签转化为列表
    :param labels:标签的字符串列表（每一串字符串末尾没有换行符）
    :return:标签的坐标列表列表
    """
    newlabels = []
    for label in labels:
        boys = label.split(" ")
        for i in range(len(boys)):
            boys[i] = float(boys[i])

        xyxyxyxy = list(boys[1:])

        p1 = xyxyxyxy[0: 2]
        p2 = xyxyxyxy[2: 4]
        p3 = xyxyxyxy[4: 6]
        p4 = xyxyxyxy[6: 8]

        newlabels.append(p1 + p2 + p3 + p4)

    return newlabels


def switch_lists2str(labels):
    """
    将坐标列表列表的标签转化为字符串列表
    :param labels:标签的坐标列表列表
    :return:标签的字符串列表
    """
    newlabels = []
    for label in labels:
        new_boy = ""
        for boy in label:
            boy = str(boy)
            new_boy += boy
            new_boy += " "

        new_boy = new_boy[:-1]
        newlabels.append(new_boy)

    return newlabels


def switch_ab(image, labels, flag):
    """
    将列表坐标在相对和绝对坐标系之间进行转换
    :param image:标签对应的图像
    :param labels:列表形式的坐标，可能是相对也可能是绝对
    :param flag:0为从相对转为绝对，1为从绝对转为相对
    :return:转换后的列表坐标
    """
    # 获取图像宽高
    height, width, _ = image.shape

    newlabels = []
    for label in labels:
        p1 = label[0: 2]
        p2 = label[2: 4]
        p3 = label[4: 6]
        p4 = label[6: 8]

        if flag == 0:
            p1[0] = int(p1[0] * width)
            p1[1] = int(p1[1] * height)
            p2[0] = int(p2[0] * width)
            p2[1] = int(p2[1] * height)
            p3[0] = int(p3[0] * width)
            p3[1] = int(p3[1] * height)
            p4[0] = int(p4[0] * width)
            p4[1] = int(p4[1] * height)
        elif flag == 1:
            p1[0] = p1[0] / width
            p1[1] = p1[1] / height
            p2[0] = p2[0] / width
            p2[1] = p2[1] / height
            p3[0] = p3[0] / width
            p3[1] = p3[1] / height
            p4[0] = p4[0] / width
            p4[1] = p4[1] / height

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


def switch_class(label_files):
    '''

    :param label_files:
    :return:
    '''
