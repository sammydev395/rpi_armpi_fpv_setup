#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第1课 机械臂人脸检测+风扇控制(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 1 face detection + fan control)
import cv2
import time
import gpiod
import mediapipe as mp
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 500]])
controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 1)
time.sleep(1)

## 初始化引脚模式(initialize pin mode)
chip = gpiod.chip("gpiochip4")
fanPin1 = chip.get_line(22)
fanPin2 = chip.get_line(24)
config = gpiod.line_request()
config.consumer = "pin1"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
fanPin1.request(config)

config = gpiod.line_request()
config.consumer = "pin2"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
fanPin2.request(config)

def runfan():
    ## 开启风扇(start fan)
    fanPin1.set_value(1) #设置引脚输出高电平(set pin output high voltage level)
    fanPin2.set_value(0) #设置引脚输出低电平(set pin output low voltage level)

def stopfan():
    ## 关闭风扇(close fan)
    fanPin1.set_value(0) #设置引脚输出高电平(set pin output high voltage level)
    fanPin2.set_value(0) #设置引脚输出低电平(set pin output low voltage level)

# 人脸检测(face detection)
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.8) #阈值(threshold value)

count_detect = 0
count_miss = 0
fan_on = False
def run(img):
    global count_detect, count_miss, fan_on

    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(img)
    img.flags.writeable = True
    if results.detections:
        for detection in results.detections:
            if detection.label_id == [0]:
                mp_drawing.draw_detection(img, detection)
                count_detect += 1
                count_miss = 0
                if count_detect > 5 and not fan_on:
                    runfan()
                    fan_on = True
                    count_detect = 0
                break
    else:
        count_detect = 0
        count_miss += 1
        if count_miss > 5 and fan_on:
            stopfan()
            fan_on = False
            count_miss = 0
    
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

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
