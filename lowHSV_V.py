# @File  : lowHSV_V.py
# @Author: horsefly
# @Time: 2024/7/14 下午2:54 
# -*- coding: utf-8 -*-

def low_hsv(dir1):
    # 拿出数据
    img_files = []
    label_files = []
    files = os.listdir(dir1)
    for file in files:
        name, suf = file.split(".")
        if suf == 'txt':
            label_files.append(file)
        else:
            img_files.append(file)

    # 遍历数据
    for i in range(len(img_files)):
        # 获取图片和标签
        img = cv.imread(os.path.join(dir1, img_files[i]))
        label = []
        temp_name, _ = img_files[i].split('.')
        if os.path.exists(os.path.join(dir1, temp_name + '.txt')) == False:
            continue
        with open(os.path.join(dir1, temp_name + '.txt'), "r") as temp_file:
            for line in temp_file:
                label.append(line)

        with open("/home/horsefly/下载/new/" + temp_name + '.txt', "w") as f:
            for line in label:
                f.write(line)

        # 获得自适应扩大的标签
        label_out = scale(img, label)

        # 对每个自适应扩大的标签区域进行随机亮度降低
        for i in range(len(label_out)):
            temp = np.float32([[label_out[i][0], label_out[i][1]], [label_out[i][2], label_out[i][3]],
                                [label_out[i][4], label_out[i][5]], [label_out[i][6], label_out[i][7]]])

            height, width, _ = img.shape
            # 制作掩膜
            mask = np.zeros((height, width), dtype=np.uint8)
            # 绘制白色矩形
            points = np.array(np.expand_dims(temp, axis=0), dtype=np.int32)
            cv.polylines(mask, points, True, (255, 255, 255, 0))
            # 填充矩形
            cv.fillPoly(mask, points, (255, 255, 255))
            # 覆盖
            roi = np.zeros((height, width, 3), dtype=np.uint8)
            cv.copyTo(img, mask, roi)
            roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            # 对roi进行随机亮度下降
            v = np.random.uniform(0.08, 0.3)
            value = roi[:, :, 2]
            new_value = value * v
            new_value = new_value.astype(np.uint8)
            new_value[new_value > 255] = 255
            new_value[new_value < 0] = 0
            roi[:, :, 2] = new_value
            roi = cv.cvtColor(roi, cv.COLOR_HSV2BGR)
            # 再利用mask将roi覆盖回去
            cv.copyTo(roi, mask, img)

        # 将图像和标签进行保存
        cv.imwrite("/home/horsefly/下载/new/" + temp_name + ".jpg", img)

