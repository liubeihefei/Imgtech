# @File  : getFiles.py
# @Author: horsefly
# @Time: 2024/6/5 下午7:16 
# -*- coding: utf-8 -*-

import os


def get_files(img_files, label_files, dirs):
    '''
    根据所给绝对路径获取图片、标签文件绝对路径列表
    :param img_files:图片绝对路径列表
    :param label_files:标签绝对路径列表
    :param dirs:绝对路径列表（若图片与标签不在同一目录，多次调用该函数即可）
    :return:none
    '''

    for dir in dirs:
        # 如果是文件，则根据后缀将完整路径放进对应列表
        if os.path.isfile(dir):
            name, suf = dir.split(".")
            if suf == "txt":
                label_files.append(dir)
            else:
                img_files.append(dir)
        # 否则递归调用
        else:
            temp = os.listdir(dir)
            for i in range(len(temp)):
                temp[i] = os.path.join(dir, temp[i])
            get_files(img_files, label_files, temp)


def find_labels(img_file, label_files, label):
    '''

    :param img_file:要找的图片的绝对路径
    :param label_files:标签的绝对路径列表
    :param label:指定要查询的类，可以为列表，当填-1时保存标签所有行
    :return:经过筛选的标签列表，每一个元素为字符串（不带换行符）；同时返回对应的标签文件绝对路径
    '''
    name, suf = img_file.split('.')

    labels = []
    label_file = ""

    # 查找标签集里是否有所要图像对应的
    name = name + ".txt"

    for i in range(len(label_files)):
        if name == label_files[i]:
            label_file = label_files[i]
            with open(label_files[i], 'r') as temp_file:
                for line in temp_file:
                    boys = line.split(' ')
                    if len(label) == 1:
                        if (int(boys[0]) == label[0] or label[0] == -1) and len(boys) == 9:
                            # 去掉讨厌的换行符
                            line = line[:-2]
                            labels.append(line)
                    else:
                        for j in range(len(label)):
                            if int(boys[0]) == label[j] and len(boys) == 9:
                                # 去掉讨厌的换行符
                                line = line[:-2]
                                labels.append(line)

    return labels, label_file


def get_classes(label_file):
    """
    根据标签文件获取类别，为字符串列表
    :param label_file:标签文件的绝对路径
    :return:类别的字符串列表
    """
    classes = []
    with open(label_file) as file:
        for line in file:
            temp = line.split(" ")
            classes.append(temp[0])

    return classes

