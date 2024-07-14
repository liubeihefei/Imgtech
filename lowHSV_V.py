# @File  : lowHSV_V.py
# @Author: horsefly
# @Time: 2024/7/14 下午2:54 
# -*- coding: utf-8 -*-

import numpy as np
import cv2


def low_hsv(img_file, labels, k):
    """
    将图片的标签区域进行随机亮度变化，从1-k —— 1+k
    :param img_file:图片的绝对路径
    :param labels:图片对应的标签的列表坐标
    :return:变化后的图片
    """
    img = cv2.imread(img_file)

    # 对每个标签区域进行随机亮度降低
    for i in range(len(labels)):
        temp = np.float32([[labels[i][0], labels[i][1]], [labels[i][2], labels[i][3]],
                            [labels[i][4], labels[i][5]], [labels[i][6], labels[i][7]]])
        height, width, _ = img.shape
        # 制作掩膜
        mask = np.zeros((height, width), dtype=np.uint8)
        # 绘制白色矩形
        points = np.array(np.expand_dims(temp, axis=0), dtype=np.int32)
        cv2.polylines(mask, points, True, (255, 255, 255, 0))
        # 填充矩形
        cv2.fillPoly(mask, points, (255, 255, 255))
        # 覆盖
        roi = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.copyTo(img, mask, roi)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # 对roi进行随机亮度变换
        v = np.random.uniform(1 - k, 1)
        value = roi[:, :, 2]
        new_value = value * v
        new_value = new_value.astype(np.uint8)
        new_value[new_value > 255] = 255
        new_value[new_value < 0] = 0
        roi[:, :, 2] = new_value
        roi = cv2.cvtColor(roi, cv2.COLOR_HSV2BGR)
        # 再利用mask将roi覆盖回去
        cv2.copyTo(roi, mask, img)

    return img
