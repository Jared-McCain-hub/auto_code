import os
import numpy as np
import cv2
from ultralytics import YOLO


class CrownDetect(object):
    def __init__(self, model_path):
        """
        :param model_path: 模型路径
        """
        super(CrownDetect).__init__()
        self.model = YOLO(model_path)

    def process_crop(self, image):
        """
        :param image: 通过opencv.imread的image或者image的路径
        :return boxes: 以图像左上角为原点的数组形式边框，[[center_x, center_y, w, h], ...]
        """
        if isinstance(image, str):
            image = cv2.imread(image)
        h, w, _ = image.shape
        image = image[:, 400:w - 500]
        results = self.model(image)
        boxes = []
        for result in results:
            shape = result.boxes.shape
            for i in range(shape[0]):
                conf = result.boxes.conf[i]
                if conf < 0.6:
                    continue
                xywh = result.boxes.xywh[i]
                bbox = xywh.cpu().numpy()
                boxes.append(bbox)
        if len(boxes)>0:
            boxes = np.vstack(boxes).astype(np.int32)
        boxes = np.vstack(boxes).astype(np.int32)
        return boxes

    def process(self, image):
        """
        :param image: 通过opencv.imread的image或者image的路径
        :return boxes: 以图像左上角为原点的数组形式边框，[[center_x, center_y, w, h], ...]
        """
        results = self.model(image)
        boxes = []
        for result in results:
            shape = result.boxes.shape
            for i in range(shape[0]):
                conf = result.boxes.conf[i]
                if conf < 0.6:
                    continue
                xywh = result.boxes.xywh[i]
                bbox = xywh.cpu().numpy()
                boxes.append(bbox)
        if len(boxes)>0:
            boxes = np.vstack(boxes).astype(np.int32)
        return boxes


if __name__ == '__main__':
    image = cv2.imread(r"D:\images\-HUANGSITING.png")
    detect = CrownDetect("CrownDetect.pt")
    boxes = detect.process(image)
    print(boxes)
    for box in boxes:
        cv2.rectangle(image, (box[0] - (box[2] // 2), box[1] - (box[3] // 2)), (box[0] + (box[2] // 2), box[1] + (box[3] // 2)), (0, 255, 0), 2)
    # cv2.imshow("", image)
    # cv2.waitKey(0)
    cv2.imwrite("CrownDetect.jpg", image)