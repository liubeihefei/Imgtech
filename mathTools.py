# @File  : mathTools.py
# @Author: horsefly
# @Time: 2024/6/5 下午9:19 
# -*- coding: utf-8 -*-


def cal_iou(a, b):
    '''
    计算两不规则四边形的iou
    :param a: 四个坐标，类型为List
    :param b: 列表，左上开始逆时针存放四个点
    :return:iou
    '''

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
