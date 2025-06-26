#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\2.AI视觉追踪\第3课 人脸定位实验ROS+OpenCV course\2. AI vision tracking\Lesson 3 face location)
import cv2
import time
import math
import mediapipe as mp
from typing import Union, Tuple
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

# 人脸检测(face detection)
board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.15, 0, 0.25], 0, [-90, 90], 0, 1)
time.sleep(1)

#先将所有灯关闭(turn off all the lights firstly)
board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.8)

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

count_detect = 0
count_miss = 0
rgb_on = False
def run(img):
    global count_detect, count_miss, rgb_on
   # point = _normalized_to_pixel_coordinates(data.xmin, data.ymin, w, h)
    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(img)
    img.flags.writeable = True
    h, w = img.shape[:2]
   # cv2.rectangle(img, (int(w/2 - w/8), 0), (int(w/2 + w/8), h), (255, 255, 0), 2)
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(img, detection)
            data = detection.location_data.relative_bounding_box
            point = _normalized_to_pixel_coordinates(data.xmin, data.ymin, w, h)
            if point is not None:
                x1, y1 = point
                width, height = _normalized_to_pixel_coordinates(data.width, data.height, w, h)
                x, y = (x1 + width / 2, y1 + height / 2)
                cv2.circle(img, (int(x), int(y)), 5, (255, 255, 0), -1)
                cv2.putText(img, "({}, {})".format(int(x),int(y)), (int(x) - int((1 + len(str(x)) + len(str(y)))*9),int(y) - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)

                if abs(x - w/2) < w/8:
                    count_detect += 1
                    count_miss = 0
                    if count_detect > 5 and not rgb_on:
                        count_detect = 0
                        rgb_on = True
                        board.set_rgb([[1, 0, 255, 255], [2, 0, 255, 255]])
                else:
                    count_detect = 0
                    count_miss += 1
                    if count_miss > 5 and rgb_on:
                        count_miss = 0
                        rgb_on = False
                        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

    else:
        count_detect = 0
        count_miss += 1
        if count_miss > 5 and rgb_on:
            count_miss = 0
            rgb_on = False
            board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])
   # cv2.putText(img, "({}, {})".format(x, y), (x - int((1 + len(str(x)) + len(str(y)))*9), y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1) 
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


