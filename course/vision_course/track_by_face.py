#!/usr/bin/env python3
# coding=utf8
# 第12章 ROS+OpenCV课程\2.AI视觉追踪\第4课 人脸追踪实验(12. ROS+OpenCV course\2. AI vision tracking\Lesson 4 human face tracking)
import cv2
import time
import math
import mediapipe as mp
from common import pid
from typing import Union, Tuple
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 500]])
controller.go_pose_target([0.15, 0, 0.25], 0, [-90, 90], 0, 1)
pid_x = pid.PID(0.15, 0, 0)
servo = 500
time.sleep(1)

# 人脸检测(face detection)
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.8) #阈值(threshold value)

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px

def run(img):
    global servo

    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(img)
    img.flags.writeable = True
    h, w = img.shape[:2]
    if results.detections:
        for detection in results.detections:
            if detection.label_id == [0]:
                mp_drawing.draw_detection(img, detection)
                data = detection.location_data.relative_bounding_box
                point = _normalized_to_pixel_coordinates(data.xmin, data.ymin, w, h)
                
                if point is not None:
                    x1, y1 = point
                    width, height = _normalized_to_pixel_coordinates(data.width, data.height, w, h)
                    x, y = (x1 + width / 2, y1 + height / 2)
                    cv2.circle(img, (int(x), int(y)), 5, (255, 255, 0), -1)
                    pid_x.SetPoint = w / 2
                    if abs(x - w/2) < 10:
                        x = w/2
                    pid_x.update(x)
                    servo += pid_x.output
                    if servo > 800:
                        servo = 800
                    if servo < 200:
                        servo = 200
                    board.bus_servo_set_position(0.02, [[6, int(servo)]])
                break
    
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
