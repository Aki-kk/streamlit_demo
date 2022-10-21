import base64
import io
import json
import PIL
import os
import numpy as np
import pandas as pd
import numpy as np
import requests
import cv2
from PIL import Image
from pandas.core.frame import DataFrame

# a = 'a'
# bytes_data = requests.post(f"http://127.0.0.1:8000/{a}").json()
# print(bytes_data)

# data = requests.get(f"http://127.0.0.1:8080/pic")
# image = Image.open(io.BytesIO(data.content))

# PATH = 'E:/dataset/a'
# pics = os.listdir(PATH)
# for pic in pics:
#     print(PATH+'/'+pic)
# PATH = 'E:/dataset/'+'a'
# pics = os.listdir(PATH)
# for i in range(len(pics)):
#     pics[i] = 'E:/dataset/'+'a' + pics[i]
#
# print(pics)
json_path = 'E:/dataset/001_test/json/0gkxrou837.json'
image_path = 'E:/dataset/001_test/json/0gkxrou837.jpg'
box_enable = True
score = 0.9
color = (0, 222, 120)
image = cv2.imread(image_path)
with open(json_path, 'r') as f:
    label_data = json.load(f)
for item in label_data["shapes"]:
    label = item["label"]
    shape = item["shape_type"]
    points = item["points"]
    if shape == 'rectangle':
        [x1, y1], [x2, y2] = points
        if box_enable:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, int(5))
        cv2.putText(image, "{}".format(label),
                    (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, int(2))
    elif shape == 'polygon':
        x0, y0 = points[0]
        x = [[]] * len(points)
        y = [[]] * len(points)
        cv2.putText(image, "{}".format(label),
                    (int(x0), int(y0) - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, int(2))
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), color, int(1))
        cv2.line(image, (int(x0), int(y0)), (int(x2), int(y2)), color, int(1))
# 创建窗口
cv2.namedWindow("Image")
# 显示图片
cv2.imshow("Image", image)
# 暂停运行，防止图片一闪而过
cv2.waitKey (0)
# 销毁窗口
cv2.destroyAllWindows()


