import cv2
from switchLabels import switch_strs2lists
import numpy as np


def mat_trans_Image(img, xyxyxyxy, target_xy):
    """
    将图片中的目标（任意四点框定）透视变换为目标长宽的图片
    :param img: 输入图片
    :param xyxyxyxy: 目标中的四点坐标（相对）
    :param target_xy: 目标图片的长宽（绝对）
    :return: 透视变换后的图片
    """
    # 定义原四个点
    src_points = np.float32([[xyxyxyxy[0], xyxyxyxy[1]], [xyxyxyxy[2], xyxyxyxy[3]],
                             [xyxyxyxy[4], xyxyxyxy[5]], [xyxyxyxy[6], xyxyxyxy[7]]])
    # 定义目标四个点
    dst_points = np.float32([[target_xy[0], target_xy[1]], [0, target_xy[1]], [0, 0], [target_xy[0], 0]])
    # 获取透视变换矩阵
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    # 进行透视变换
    new_img = cv2.warpPerspective(img, matrix, (target_xy[0], target_xy[1]))

    return new_img


def split_Image(img, xyxy):
    """
    根据给定的左上右下两点确定的矩形位置裁剪img
    :param img: 待裁剪图像
    :param xyxy: [x，y，x，y]
    :return:裁剪后的图像
    """
    new_img = img[xyxy[1]: xyxy[3], xyxy[0]: xyxy[2]]

    return new_img


def scale_Image(img, target_wh):
    """
    将图像缩放至目标长宽
    :param img:原图像
    :param target_wh:目标长宽
    :return:缩放后的图像
    """
    # resize中默认双线性插值（cv2.INTER_LINEAR）
    new_img = cv2.resize(img, [target_wh[0], target_wh[1]])
    return new_img


if __name__ == '__main__':
    img = cv2.imread("/media/horsefly/新加卷/数据集/NEW_CCPD2020/test/19.jpg")
    xyxyxyxy = [0.8444444444444444, 0.46206896551724136, 0.37222222222222223, 0.44396551724137934,
                0.3375, 0.3706896551724138, 0.8305555555555556, 0.3775862068965517]
    height, width, _ = img.shape
    for i in range(4):
        xyxyxyxy[2 * i] *= width
        xyxyxyxy[2 * i + 1] *= height
    new_img = mat_trans_Image(img, xyxyxyxy, [88, 28])
    cv2.imwrite("/home/horsefly/下载/temp/mat1.jpg", new_img)

    # img = cv2.imread("/media/horsefly/新加卷/数据集/NEW_CCPD2020/test/11.jpg")
    # xyxyxyxy = [0.7569444444444444, 0.5275862068965518, 0.29583333333333334, 0.5224137931034483,
    #             0.2708333333333333, 0.44568965517241377, 0.7486111111111111, 0.44482758620689655]
    # height, width, _ = img.shape
    # for i in range(4):
    #     xyxyxyxy[2 * i] *= width
    #     xyxyxyxy[2 * i + 1] *= height
    # new_img = mat_trans_Image(img, xyxyxyxy, [88, 28])
    # cv2.imwrite("/home/horsefly/下载/temp/mat1.jpg", new_img)



    nnew_img = split_Image(new_img, np.array([3, 5, 12, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat1.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([14.5, 5, 23.4, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat2.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([30.2, 5, 39.2, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat3.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([41.6, 5, 48.8, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat4.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([51.2, 5, 58.4, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat5.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([60.8, 5, 68, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat6.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([70.4, 5, 77.6, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat7.jpg", nnew_img)

    nnew_img = split_Image(new_img, np.array([80, 5, 87.2, 23], np.int32))
    cv2.imwrite("/home/horsefly/下载/temp/split_mat8.jpg", nnew_img)
