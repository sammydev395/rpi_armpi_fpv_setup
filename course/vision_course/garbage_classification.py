#!/usr/bin/python3
# coding=utf8
# 第13章 ArmPi FPV创意玩法课程\3.语音交互玩法课程\第4课 语音播报垃圾分类(13. ArmPi FPV creative application course\3. voice interaction course\Lesson 4 voice broadcasting of garbage classification)
import os
import cv2
import math
import time
import threading
import numpy as np
from sensor.tts_sensor import TTS
from common.yaml_handle import get_yaml_data
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
lab_data = get_yaml_data(os.path.join(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../sensor_course/sensor_with_arm')), 'lab_config.yaml'))['color_range_list']
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.1], 90, [-90, 90], 0, 1)

try:
    tts = TTS()
except:
    print('没有接tts传感器')

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'gray': (50, 50, 50),
    'None': (0, 0, 0)}

garbage_dict = {'Hazardous Waste': '有害垃圾',
                'Food Waste': '厨余垃圾',
                'Recyclable': '可回收垃圾',
                'Residual Waste': '其他垃圾'}

#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致(set the color of RGB light on the expansion board to match the tracking color)
def set_rgb(color):
    if color == "red":
        board.set_rgb([[1, 255, 0, 0], [2, 255, 0, 0]])
    elif color == "green":
        board.set_rgb([[1, 0, 255, 0], [2, 0, 255, 0]])
    elif color == "blue":
        board.set_rgb([[1, 0, 0, 255], [2, 0, 0, 255]])
    else:
        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

# 找出面积最大的轮廓(find out the contour with the largest area)
# 参数为要比较的轮廓的列表(the parameter is a list of contours to compare)
def getAreaMaxContour(contours):
    
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  # 历遍所有轮廓(iterate through all contours)
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积(calculate contour area)
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰(only when contours with an area greater than 300 are considered valid, and the contour with the maximum area is used to filter out interference)
                area_max_contour = c

    return area_max_contour, contour_area_max  # 返回最大的轮廓(return the largest contour)

garbage_species = 'None'
detect_color = 'None'
def speaker():
    global garbage_species, detect_color
    
    while True:
        if garbage_species != 'None':
            tts.TTSModuleSpeak("[h0][v10][m52]", garbage_dict[garbage_species])
            time.sleep(2)
            detect_color = 'None'
            garbage_species = 'None'
        else:
            time.sleep(0.01)
      
# 运行子线程(run sub threat)
th = threading.Thread(target=speaker)
th.setDaemon(True)
th.start()

color_list = []
def run(img):
    global garbage_species, detect_color, color_list

    frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间(convert image to the LAB space)
    color_area_max = None
    max_area = 0
    areaMaxContour_max = 0
    
    for i in __target_color:
        if i in lab_data:
            frame_mask = cv2.inRange(frame_lab,
                                         (lab_data[i]['min'][0],
                                          lab_data[i]['min'][1],
                                          lab_data[i]['min'][2]),
                                         (lab_data[i]['max'][0],
                                          lab_data[i]['max'][1],
                                          lab_data[i]['max'][2]))  #对原图像和掩模进行位运算(perform bitwise operations on the original image and the mask)
            opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算(opening operation)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算(closing operation)
            contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓(find out contour)
            areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓(find out the largest contour)
            if areaMaxContour is not None:
                if area_max > max_area:  # 找最大面积(find the largest area)
                    max_area = area_max
                    color_area_max = i
                    areaMaxContour_max = areaMaxContour
        
    if max_area > 500:  # 有找到最大面积(the largest area is found)
        rect = cv2.minAreaRect(areaMaxContour_max)
        box = np.int0(cv2.boxPoints(rect))
        
        cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
        if color_area_max == 'red':  # 红色最大(rea maximum)
            color = 1
        elif color_area_max == 'green':  # 绿色最大(green maximum)
            color = 2
        elif color_area_max == 'blue':  # 蓝色最大(blue maximum)
            color = 3
        elif color_area_max == 'gray':  # 蓝色最大(blue maximum)
            color = 4
        else:
            color = 0
        color_list.append(color)
        if len(color_list) == 20:  # 多次判断(determine in multiple times)
            # 取平均值(take average value)
            color = int(round(np.mean(np.array(color_list))))
            color_list = []
            
            if color == 1:
                detect_color = 'red'
                set_rgb(detect_color)
                garbage_species = 'Hazardous Waste'
            elif color == 2:
                detect_color = 'green'                      
                set_rgb(detect_color)
                garbage_species = 'Food Waste'
            elif color == 3:
                detect_color = 'blue'
                set_rgb(detect_color)
                garbage_species = 'Recyclable'
            elif color == 4:
                detect_color = 'gray'                        
                set_rgb(detect_color)
                garbage_species = 'Residual Waste'
            else:
                detect_color = 'None'
                set_rgb(detect_color)
     
    cv2.putText(img, "Label: " + garbage_species, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, range_rgb[detect_color], 2)
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
    __target_color = ('red', 'green', 'blue', 'gray')
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

        
