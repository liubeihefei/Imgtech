# @File  : showLabels.py
# @Author: horsefly
# @Time: 2024/6/7 下午7:55 
# -*- coding: utf-8 -*-

import os
import cv2

from getFiles import get_files, find_labels, get_classes
from switchLabels import switch_strs2lists, switch_ab, switch_lists2str
from mathTools import scale
from saveFiles import saveImgAndLabels
from lowHSV_V import low_hsv


def show_label(img, label, dir):
    '''
    根据所给图片和标签，将四点格式的标签绘制在图上并保存到路径dir处
    :param img: 图片文件路径
    :param label: 对应的标签文件路径
    :param dir: 保存路径
    :return:none
    '''

    # 获取名字
    name, suf = img.split(".")
    name = name.split("/")[-1]

    # 读取图片，获得宽高
    image = cv2.imread(img)
    height, width, _ = image.shape

    # 将标签转化为四个坐标形式
    labels = []
    with open(label) as file:
        for line in file:
            labels.append(line[:-2])
    new_labels = switch_strs2lists(labels)
    new_labels = switch_ab(image, new_labels, 0)

    # 将四点绘制在图上并保存
    for nl in new_labels:
        cv2.line(image, (nl[0], nl[1]), (nl[2], nl[3]), (0, 0, 255), 1)
        cv2.line(image, (nl[2], nl[3]), (nl[4], nl[5]), (0, 255, 0), 1)
        cv2.line(image, (nl[4], nl[5]), (nl[6], nl[7]), (255, 0, 255), 1)
        cv2.line(image, (nl[6], nl[7]), (nl[0], nl[1]), (255, 255, 255), 1)
    cv2.imwrite(dir + "/" + name + "." + suf, image)



if __name__ == '__main__':
    # 获取图片和标签文件
    img_files = []
    label_files = []
    dirs = os.listdir("/home/horsefly/下载/test")
    for i in range(len(dirs)):
        dirs[i] = os.path.join("/home/horsefly/下载/test", dirs[i])
    get_files(img_files, label_files, dirs)

    dir = "/home/horsefly/下载/temp"

    cnt = 0

    for img_file in img_files:
        labels, label_file = find_labels(img_file, label_files, [-1])
        labels = switch_strs2lists(labels)
        labels = switch_ab(cv2.imread(img_file), labels, 0)

        new_img = low_hsv(img_file, labels, 0.8)
        cv2.imwrite(dir + "/out" + str(cnt) + ".jpg", new_img)
        cnt += 1

        # # 获取类别
        # classes = get_classes(label_file)
        #
        # new_labels = scale(labels, 1.2, 1.2)
        # new_labels = switch_ab(cv2.imread(img_file), new_labels, 1)
        # new_labels = switch_lists2str(new_labels)
        # saveImgAndLabels(img_file, new_labels, classes, dir)

    # show_label("/home/horsefly/下载/rune/train/official/OFFICIAL_23_RUNE_5.jpg", "/home/horsefly/下载/rune/train/official/OFFICIAL_23_RUNE_5.txt", "/home/horsefly/下载")

