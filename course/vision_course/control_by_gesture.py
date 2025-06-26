#!/usr/bin/env python3
# encoding: utf-8
# 第13章 ArmPi FPV创意玩法课程\1.AI视觉创意玩法\第6课 手势识别堆积木(13. ArmPi FPV creative application course\1. AI vision creative course\Lesson 6 gesture-guided goods stacking)
import cv2
import time
import threading
import numpy as np
import mediapipe as mp
import common.fps as fps
from common.ros_robot_controller_sdk import Board
from common.transform import vector_2d_angle, distance
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 1)
time.sleep(1)

def get_hand_landmarks(img, landmarks):
    """
    将landmarks从medipipe的归一化输出转为像素坐标(convert landmarks from the normalized output of mediapipe to pixel coordinates)
    :param img: 像素坐标对应的图片(the image corresponding to the pixel coordinates)
    :param landmarks: 归一化的关键点(normalized keypoint)
    :return:
    """
    h, w, _ = img.shape
    landmarks = [(lm.x * w, lm.y * h) for lm in landmarks]
    return np.array(landmarks)

def hand_angle(landmarks):
    """
    计算各个手指的弯曲角度(calculate the bending angle of each finger)
    :param landmarks: 手部关键点(hand keypoint)
    :return: 各个手指的角度(each finger angle)
    """
    angle_list = []
    # thumb 大拇指
    angle_ = vector_2d_angle(landmarks[3] - landmarks[4], landmarks[0] - landmarks[2])
    angle_list.append(angle_)
    # index 食指
    angle_ = vector_2d_angle(landmarks[0] - landmarks[6], landmarks[7] - landmarks[8])
    angle_list.append(angle_)
    # middle 中指
    angle_ = vector_2d_angle(landmarks[0] - landmarks[10], landmarks[11] - landmarks[12])
    angle_list.append(angle_)
    # ring 无名指
    angle_ = vector_2d_angle(landmarks[0] - landmarks[14], landmarks[15] - landmarks[16])
    angle_list.append(angle_)
    # pink 小拇指
    angle_ = vector_2d_angle(landmarks[0] - landmarks[18], landmarks[19] - landmarks[20])
    angle_list.append(angle_)
    angle_list = [abs(a) for a in angle_list]
    return angle_list

def h_gesture(angle_list):
    """
    通过二维特征确定手指所摆出的手势(determine the gesture formed by the fingers using 2D features)
    :param angle_list: 各个手指弯曲的角度(the bending angle of each finger)
    :return : 手势名称字符串(gesture name string)
    """
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = "none"
    if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "fist"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "hand_heart"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
        gesture_str = "nico-nico-ni"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "hand_heart"
    elif (angle_list[0] > 5) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "one"
    elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "two"
    elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
        gesture_str = "three"
    elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
        gesture_str = "OK"
    elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
        gesture_str = "four"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
        gesture_str = "five"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
        gesture_str = "six"
    else:
        "none"
    return gesture_str

def action(times=1):
    for i in range(times):
        controller.go_pose_target([0, 0.1, 0.18], 0, [-90, 90], 0, 1.5)
        time.sleep(1.5)
        controller.go_pose_target([0, 0.12, 0.01], 90, [-90, 90], 0, 1.5)
        time.sleep(1.5)
        board.bus_servo_set_position(0.8, [[1, 500]])
        time.sleep(1)
        controller.go_pose_target([0, 0.1, 0.18], 0, [-90, 90], 0, 1.5)
        time.sleep(1.5)
        controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 1.5)
        time.sleep(1.5)
        controller.go_pose_target([0.12, 0, 0.012 + i*0.03], 90, [-90, 90], 0, 1.5)
        time.sleep(1.5)
        board.bus_servo_set_position(0.8, [[1, 200]])
        time.sleep(1)
        controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 1.5)
        time.sleep(1.5)

class HandGestureNode:
    def __init__(self):
        self.drawing = mp.solutions.drawing_utils

        self.hand_detector = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_tracking_confidence=0.05,
            min_detection_confidence=0.6
        )
        
        self.count = 0
        self.action_finish = True
        self.last_geture = 'none'
        self.gesture = 'none'
        self.fps = fps.FPS()  # fps计算器
        self.cap = cv2.VideoCapture(-1)
        threading.Thread(target=self.action_thread, daemon=True).start()
        self.image_proc()

    def action_thread(self):
        while True:
            if not self.action_finish and self.gesture in ['one', 'two', 'three', 'four', 'five']:
                board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
                board.bus_servo_set_position(0.8, [[1, 200]])
                time.sleep(1)
                if self.gesture == 'one':
                    action(1)
                elif self.gesture == 'two':
                    action(2)
                elif self.gesture == 'three':
                    action(3)
                elif self.gesture == 'four':
                    action(4)
                elif self.gesture == 'five':
                    action(5)
                self.action_finish = True
                self.gesture = 'none'
            else:
                time.sleep(0.01)

    def image_proc(self):
        while True:
            ret, image = self.cap.read()
            if ret:
                image_flip = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                result_image = image_flip.copy()
                try:
                    gesture = "none"
                    results = self.hand_detector.process(image_flip)
                    if results is not None and results.multi_hand_landmarks:
                        gesture = "none"
                        index_finger_tip = [0, 0]
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.drawing.draw_landmarks(
                                result_image,
                                hand_landmarks,
                                mp.solutions.hands.HAND_CONNECTIONS)
                            landmarks = get_hand_landmarks(image_flip, hand_landmarks.landmark)
                            angle_list = (hand_angle(landmarks))
                            gesture = (h_gesture(angle_list))
                            cv2.putText(result_image, gesture, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    if gesture == self.last_geture and gesture != 'none' and self.action_finish:
                        self.count += 1
                        if self.count >= 3:
                            self.action_finish = False
                            self.gesture = gesture
                            self.count = 0

                    self.last_geture = gesture
                    self.fps.update()
                    result_image = self.fps.show_fps(result_image)
                    result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
                    cv2.imshow('hand_gesture', cv2.resize(result_image, (640, 480)))
                    key = cv2.waitKey(1)
                    if key == 27:
                        break
                except Exception as e:
                    print(e)

if __name__ == "__main__":
    print('\n******Press any key to exit!******')
    HandGestureNode()
