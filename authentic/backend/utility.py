import json
import cv2

def draw_lable(image_path, json_path, color):
    # json_path = 'E:/dataset/001_test/json/0gkxrou837.json'
    # image_path = 'E:/dataset/001_test/json/0gkxrou837.jpg'
    box_enable = True
    score = 0.9
    # color = (0, 222, 120)
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
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), color, int(1))
            cv2.line(image, (int(x0), int(y0)), (int(x2), int(y2)), color, int(1))
    return image