# @File  : collectLittleTarget.py
# @Author: horsefly
# @Time: 2024/6/5 下午7:50 
# -*- coding: utf-8 -*-
import os

import cv2
import math

from mathTools import cal_iou
from getFiles import get_files, find_labels
from switchLabels import switch_strs2lists


def split_img(image, nums):
    '''
    根据所给图片以及分割数，返回分割后的小图
    :param image:需要分割的图的绝对路径
    :param nums:分割数
    :return:放大为原图大小的小图列表，每个元素为opencv里的Mat类型
    '''

    # 获取图像宽高
    height, width, _ = image.shape

    # 获取横纵方向上的步长
    ws = int(width / nums)
    hs = int(height / nums)

    # 对图像进行分割
    imgs = []
    i = 0
    j = 0
    while(i < nums):
        while(j < nums):
            # 获取roi
            roi = image[j * hs:j * hs + hs, i * ws:i * ws + ws]
            imgs.append(roi)
            j = j + 1
        i = i + 1
        j = 0

    return imgs


def collect_right_imgs(image, imgs, labels, thresh, ith, dir):
    '''
    利用已有的标签收集大致的小图
    :param image: 原图
    :param imgs: 分割后的小图
    :param labels: 标签列表的列表
    :param thresh: iou阈值，只返回大
    :param ith: 用于取名
    :param dir: 保存的地址
    :return:none
    '''

    # 获取图像宽高
    height, width, _ = image.shape

    # 获取横纵方向上的步长
    nums = int(math.sqrt(len(imgs)))
    ws = int(width / nums)
    hs = int(height / nums)

    # 保存一手原图分割宫格与实际标签矩形图
    temp_img = img.copy()
    nums = int(math.sqrt(len(imgs)))
    for i in range(nums):
        if i == 0:
            continue
        cv2.line(temp_img, (0, i * hs), (width, i * hs), (0, 255, 0), 1)
        cv2.line(temp_img, (i * ws, 0), (i * ws, height), (0, 255, 0), 1)
    for label in labels:
        cv2.line(temp_img, (label[0], label[1]), (label[2], label[3]), (0, 0, 255), 1)
        cv2.line(temp_img, (label[2], label[3]), (label[4], label[5]), (0, 255, 0), 1)
        cv2.line(temp_img, (label[4], label[5]), (label[6], label[7]), (255, 0, 255), 1)
        cv2.line(temp_img, (label[6], label[7]), (label[0], label[1]), (255, 255, 255), 1)
    cv2.imwrite(dir + "/ori/" + str(ith) + ".jpg", temp_img)

    # 依次计算每个宫格与标签构成矩形的iou，将iou大于阈值的小图保存
    cnt = 0
    for label in labels:
        i = 0
        j = 0
        while (i < nums):
            while (j < nums):
                b = [i * ws, j * hs, i * ws, j * hs + hs,
                     i * ws + ws, j * hs + hs, i * ws + ws, j * hs]
                iou = cal_iou(label, b)
                if iou > thresh:
                    cv2.imwrite(dir + "/" + str(ith) + "_" + str(cnt) + ".jpg", cv2.resize(imgs[i * nums + j], (width, height)))
                    cnt = cnt + 1
                j = j + 1
            i = i + 1
            j = 0


if __name__ == '__main__':
    # 获取图片和标签文件
    img_files = []
    label_files = []
    dirs = os.listdir("/home/horsefly/下载/final_ydd_xyxyxyxy")
    for i in range(len(dirs)):
        dirs[i] = os.path.join("/home/horsefly/下载/final_ydd_xyxyxyxy", dirs[i])
    get_files(img_files, label_files, dirs)

    # 对图像进行遍历
    cnt = 0
    for img_dir in img_files:
        # 获取当前图片和标签
        img = cv2.imread(img_dir)
        labels = find_labels(img_dir, label_files, [-1])

        # 将标签转化为List
        new_labels = switch_strs2lists(img, labels)

        # 对当前图像进行分割，按8倍下分
        imgs = split_img(img, 4)

        # 进行保存
        dir = "/home/horsefly/下载/temp"
        collect_right_imgs(img, imgs, new_labels, 0.0, cnt, dir)

        cnt = cnt + 1
