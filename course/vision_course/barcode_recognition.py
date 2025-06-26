#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\1.AI视觉识别\第8课 条形码识别实验(12. ROS+OpenCV course\1. AI recognition course\Lesson 8 barcode recognition)
import cv2
from pyzbar import pyzbar

def run(image):
    # 找到图像中的条形码并解码每个条形码(find the barcode in the image and decode each barcode)
    barcodes = pyzbar.decode(image)
    # 循环检测到的条形码(look through detected barcode)
    for barcode in barcodes:
        # 提取条形码的边界框位置(extract the bounding box positions of the barcodes)
        (x, y, w, h) = barcode.rect
        # 绘出图像上条形码的边框(draw the bounding boxes of the barcodes on the image)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # 在图像上绘制条形码数据和条形码类型(draw the barcode data and barcode type in diagram)
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return image

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
    while True:
        ret, img = cap.read()
        if ret:
            frame = run(img)           
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
