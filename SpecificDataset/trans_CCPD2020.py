# @File  : trans_CCPD2020.py
# @Author: horsefly
# @Time: 2025/5/29 下午3.03
# -*- coding: utf-8 -*-

import os
from PIL import Image
import cv2

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


if __name__ == '__main__':
    img_files_dir = "/home/horsefly/CCPD2020/ccpd_green/test"
    new_files_dir = "/home/horsefly/NEW_CCPD2020/test"

    trans_Image(img_files_dir, new_files_dir)
