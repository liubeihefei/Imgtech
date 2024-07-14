import cv2


def saveImgAndLabels(img_file, labels, classes, dir):
    """
    将图片和对应的标签（字符串类型）保存到指定的dir处
    :param img_file:图片的绝对路径
    :param labels:字符串类型的标签
    :param classes:标签的类别，为字符串列表
    :param dir:指定的新路径（即只能将图片和标签保存在同一目录下）
    :return:
    """
    # 获取图片的名字
    name, suf = img_file.split(".")
    name = name.split("/")[-1]

    # 获取图片并保存到新路径
    cv2.imwrite(dir + "/" + name + ".jpg", cv2.imread(img_file))

    # 将标签进行保存
    with open(dir + "/" + name + ".txt", "w") as file:
        for i in range(len(labels)):
            file.writelines(classes[i] + " " + labels[i] + "\n")

