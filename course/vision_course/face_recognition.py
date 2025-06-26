#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\1.AI视觉识别\第5课 人脸检测实验(12. ROS+OpenCV course\1. AI vision recognition\Lesson 5 face detection experiment)
import cv2
import time
import mediapipe as mp
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.15, 0, 0.25], 0, [-90, 90], 0, 1)
time.sleep(1)

# 人脸检测(face detection)
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.8) #阈值(threshold value)

def run(img):

    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(img)
    img.flags.writeable = True
    h, w = img.shape[:2]
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(img, detection)

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
