# @File  : mathTools.py
# @Author: horsefly
# @Time: 2024/6/5 下午9:19 
# -*- coding: utf-8 -*-

import math


def cal_iou(a, b):
    """
    计算两不规则四边形的iou
    :param a: 四个坐标，类型为List
    :param b: 列表，左上开始逆时针存放四个点
    :return:iou
    """

    # 计算a的外接矩形
    ax_max = max(max(max(a[0], a[2]), a[4]), a[6])
    ax_min = min(min(min(a[0], a[2]), a[4]), a[6])
    ay_max = max(max(max(a[1], a[3]), a[5]), a[7])
    ay_min = min(min(min(a[1], a[3]), a[5]), a[7])

    # 计算b的外接矩形
    bx_max = b[6]
    bx_min = b[0]
    by_max = b[5]
    by_min = b[1]

    max_x = max(ax_min, bx_min)
    min_x = min(ax_max, bx_max)
    max_y = max(ay_min, by_min)
    min_y = min(ay_max, by_max)

    if min_x <= max_x or min_y <= max_y:
        return 0

    over_area = (min_x - max_x) * (min_y - max_y)
    area_a = (ax_max - ax_min) * (ay_max - ay_min)
    area_b = (bx_max - bx_min) * (by_max - by_min)
    iou = over_area / (area_a + area_b - over_area)

    return iou


def scale(labels, k_x, k_y):
    """
    此函数目前还有问题
    将坐标放大/缩小为原来的K倍，是按中心原地放大/缩小，不影响形状与中心位置
    :param labels:标签，为坐标列表（为绝对坐标）
    :param k_x:像素坐标系x方向缩放倍数，1为不变
    :param k_y:像素坐标系y方向缩放倍数，1为不变
    :return:缩放后标签，也是坐标列表
    """
    output_labels = []

    for label in labels:
        # 获取四个角点坐标
        p1 = label[0: 2]
        p2 = label[2: 4]
        p3 = label[4: 6]
        p4 = label[6: 8]

        # 纵向拉长p1，p2
        length1 = pow((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]), 0.5)
        if p2[0] - p1[0] != 0:
            theta1 = math.atan((p2[1] - p1[1]) / (p2[0] - p1[0]))
        else:
            theta1 = 3.1415926 / 2
        det1_y = int(length1 * k_y * math.sin(theta1))
        det1_x = int(length1 * k_x * math.cos(theta1))
        p1[1] -= det1_y
        p2[1] += det1_y
        p1[0] -= det1_x
        p2[0] += det1_x


        # 纵向拉长p4，p3
        length2 = pow((p4[0] - p3[0]) * (p4[0] - p3[0]) + (p4[1] - p3[1]) * (p4[1] - p3[1]), 0.5)
        if p3[0] - p4[0] != 0:
            theta2 = math.atan((p3[1] - p4[1]) / (p3[0] - p4[0]))
        else:
            theta2 = 3.1415926 / 2
        det2_y = int(length2 * k_y * math.sin(theta2))
        det2_x = int(length2 * k_x * math.cos(theta2))
        p4[1] -= det2_y
        p3[1] += det2_y
        p4[0] -= det2_x
        p3[0] += det2_x


        # 横向拉长p1，p4
        length3 = pow((p1[0] - p4[0]) * (p1[0] - p4[0]) + (p1[1] - p4[1]) * (p1[1] - p4[1]), 0.5)
        theta3 = math.atan((p1[1] - p4[1]) / (p1[0] - p4[0]))
        det3_x = int(length3 * k_y * math.cos(theta3))
        det3_y = int(length3 * k_x * math.sin(theta3))
        p1[0] += det3_x
        p4[0] -= det3_x
        p1[1] -= det3_y
        p4[1] += det3_y


        # 横向拉长p2，p3
        length4 = pow((p2[0] - p3[0]) * (p2[0] - p3[0]) + (p2[1] - p3[1]) * (p2[1] - p3[1]), 0.5)
        theta4 = math.atan((p2[1] - p3[1]) / (p2[0] - p3[0]))
        det4_x = int(length4 * k_y * math.cos(theta4))
        det4_y = int(length4 * k_x * math.sin(theta4))
        p2[0] += det4_x
        p3[0] -= det4_x
        p2[1] -= det4_y
        p3[1] += det4_y


        output_labels.append(p1 + p2 + p3 + p4)

    return output_labels
