# @File  : trans_CCPD2020.py
# @Author: horsefly
# @Time: 2025/5/29 下午3.03
# -*- coding: utf-8 -*-

import os
from PIL import Image
import cv2
from transImage import mat_trans_Image, split_Image, scale_Image
import numpy as np


def trans_Image(img_files_dir, new_files_dir):
    """
    将CCPD的数据转化成图片+标签的yolo格式
    :param img_files_dir:图片目录的绝对路径
    :param new_files_dir:新图片和标签绝对路径
    :return:none
    """
    # 计数器，用于命名（有点ugly）
    cnt = 0

    # 获取每张图片的绝对路径
    temp = os.listdir(img_files_dir)
    for i in range(len(temp)):
        temp[i] = os.path.join(img_files_dir, temp[i])

    for dir in temp:
        print(dir)
        # 如果是图片
        if os.path.isfile(dir):
            # 获取图片名字
            name, suf = dir.split(".")

            # 按照CCPD格式将名字（name）中的四点坐标提取出来
            all_coor = name.split("-")[3]
            # 进一步将四个角点区分开
            coors = all_coor.split("_")
            xyxyxyxy = []
            for coor in coors:
                # 进一步得到8个x/y
                xyxyxyxy.append(coor.split("&"))

            new_xyxyxyxyxy = []
            # 将xy转换成相对坐标，先打开图片文件
            image = Image.open(dir)
            # 获取图片的长宽
            width, height = image.size
            for i in range(4):
                new_xyxyxyxyxy.append(float(xyxyxyxy[i][0]) / width)
                new_xyxyxyxyxy.append(float(xyxyxyxy[i][1]) / height)

            # 将坐标转化为标签所需的形式
            label = ""
            for temp in new_xyxyxyxyxy:
                label = label + str(temp) + " "
            label = label[:-1]

            # 保存图片和标签
            cv2.imwrite(new_files_dir + "/" + str(cnt) + ".jpg", cv2.imread(dir))
            # 将标签进行保存
            with open(new_files_dir + "/" + str(cnt) + ".txt", "w") as file:
                # 这里类别不进行划分，全填0
                file.writelines("0" + " " + label + "\n")

            cnt = cnt + 1


def collect_Image(img_files_dir, new_files_dir):
    """
    收集图像中四点框定车牌中各字符的小图，涉及透视变换和裁剪
    :param img_files_dir: 原图像目录
    :param new_files_dir: 目标图像目录
    :return:
    """
    # 计数器，用于命名（此时是对应所有类的列表，但依旧ugly）
    # 省份、字母、数字（31、24、10）
    provinces_cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    letter_cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    digit_cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 处理目标路径，因为需要将省份、字母和数字分开存
    provinces_dir = new_files_dir + "/provinces"
    if not os.path.exists(provinces_dir):
        os.makedirs(provinces_dir)
    letter_dir = new_files_dir + "/letter"
    if not os.path.exists(letter_dir):
        os.makedirs(letter_dir)
    digit_dir = new_files_dir + "/digit"
    if not os.path.exists(digit_dir):
        os.makedirs(digit_dir)

    # 获取每张图片的绝对路径
    temp = os.listdir(img_files_dir)
    for i in range(len(temp)):
        temp[i] = os.path.join(img_files_dir, temp[i])

    for dir in temp:
        print(dir)
        # 如果是图片
        if os.path.isfile(dir):
            # 获取图片名字
            name, suf = dir.split(".")

            # 获取图片目标的四个角点
            img = cv2.imread(dir)
            height, width, _ = img.shape
            coors = name.split("-")[3].split("_")
            xyxyxyxy = []
            for i in range(4):
                x, y = (coors[i].split("&"))
                xyxyxyxy.append(int(x))
                xyxyxyxy.append(int(y))

            # 按照CCPD格式将省份、字母、数字提取出来
            classes = name.split("-")[4]
            province_class = classes.split("_")[0]
            letter_digit_class = []
            for i in range(7):
                letter_digit_class.append(classes.split("_")[i + 1])

            # 对图像进行透视变换和分割
            new_img = mat_trans_Image(img, xyxyxyxy, [88, 28])
            cv2.imwrite("/home/horsefly/下载/temp/trans_test.jpg", new_img)

            # 保存省份
            img1 = split_Image(new_img, np.array([3, 5, 12, 23], np.int32))
            cv2.imwrite(provinces_dir + "/" + str(provinces_cnt[int(province_class)]) +
                        "_" + province_class + ".jpg", img1)
            provinces_cnt[int(province_class)] += 1

            # 裁剪区域
            # temp_coor = np.array([[14.5, 5, 23.4, 23], [30.2, 5, 39.2, 23], [41.6, 5, 48.8, 23], [51.2, 5, 58.4, 23],
            #                             [60.8, 5, 68, 23], [70.4, 5, 77.6, 23], [80, 5, 87.2, 23]], np.int32)
            # 左右各扩展一个像素点，尽可能包含字符
            temp_coor = np.array([[13.5, 5, 24.4, 23], [29.2, 5, 40.2, 23], [40.6, 5, 49.8, 23], [50.2, 5, 59.4, 23],
                                  [59.8, 5, 69, 23], [69.4, 5, 78.6, 23], [79, 5, 88.2, 23]], np.int32)
            # 保存字母和数字
            for i in range(7):
                if int(letter_digit_class[i]) <= 23:
                    # 如果是字母，则保存到字母对应的目录
                    temp_dir = letter_dir
                    # 获取该字母对应的类编号
                    temp_cls = int(letter_digit_class[i])
                    # 获取该字母现有的数量
                    temp_cnt = letter_cnt[temp_cls]
                    # 数量加1
                    letter_cnt[temp_cls] += 1
                else:
                    # 否则保存到数字对应的目录
                    temp_dir = digit_dir
                    # 获取该数字对应的数字编号
                    temp_cls = int(letter_digit_class[i]) - 24
                    # 获取该数字现有的数量
                    temp_cnt = digit_cnt[temp_cls]
                    # 数量加1
                    digit_cnt[temp_cls] += 1
                # 裁剪
                temp_img = split_Image(new_img, temp_coor[i])
                # 缩放成9*18大小
                temp_img = scale_Image(temp_img, [9, 18])
                cv2.imwrite(temp_dir + "/" + str(temp_cnt) + "_" + str(temp_cls) + ".jpg", temp_img)


if __name__ == '__main__':
    # 构造四点数据集
    # img_files_dir = "/home/horsefly/CCPD2020/ccpd_green/test"
    # new_files_dir = "/home/horsefly/NEW_CCPD2020/test"
    #
    # trans_Image(img_files_dir, new_files_dir)

    # 构造字符分类数据集
    img_files_dir = "/home/horsefly/CCPD2020/ccpd_green/test"
    new_files_dir = "/home/horsefly/NEW_CCPD2020_COLLECT/test"

    collect_Image(img_files_dir, new_files_dir)
