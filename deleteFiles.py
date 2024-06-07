# @File  : deleteFiles.py
# @Author: horsefly
# @Time: 2024/6/7 下午7:22 
# -*- coding: utf-8 -*-

import os

from getFiles import get_files


def delete_redun_imgs(img_files, label_files):
    '''
    根据图片和标签的绝对路径列表进行一一对应，将没有标签的图片删掉
    :param img_files:图片绝对路径列表
    :param label_files:标签绝对路径列表
    :return:none
    '''

    for img_file in img_files:
        # 获取前缀
        name, suf = img_file.split(".")
        new_name = name + ".txt"

        # 遍历标签文件查看是否有对应标签
        flag = False
        for label_file in label_files:
            if label_file == new_name:
                flag = True

        # 若没有找到对应标签，则删掉图片文件
        if not flag:
            os.remove(img_file)



if __name__ == '__main__':
    # 获取图片和标签文件
    img_files = []
    label_files = []
    dirs = os.listdir("/home/horsefly/下载/gl_done（复件）")
    for i in range(len(dirs)):
        dirs[i] = os.path.join("/home/horsefly/下载/gl_done（复件）", dirs[i])
    get_files(img_files, label_files, dirs)

    # 删除多余的图片
    delete_redun_imgs(img_files, label_files)


