#!/usr/bin/env python3
# encoding: utf-8
# @data:2024/01/29
# @author:aiden
# 实时获取角度反馈，根据当前位置和
# 目标位置的最小差值来获取最优解
import numpy as np
from kinematics.common import Pose
import kinematics.transform as transform
from kinematics.forward_kinematics import ForwardKinematics 
from kinematics.inverse_kinematics import get_ik, set_link, get_link, set_joint_range, get_joint_range

fk = ForwardKinematics(debug=False)  # 不开启打印
class KinematicsController:
    def __init__(self, board):
        self.board = board

    def set_link(self, base_link, link1, link2, link3, end_effector_link):
        # 设置link长度
        set_link(base_link, link1, link2, link3, end_effector_link)
        fk.set_link(base_link, link1, link2, link3, end_effector_link)

    def get_link(self):
        # 获取各个link长度
        data = get_link()
        data1 = fk.get_link()
        if data == data1:
            base_link = data[0]
            link1 = data[1]
            link2 = data[2]
            link3 = data[3]
            end_effector_link = data[4]
            return [True, [base_link, link1, link2, link3, end_effector_link]]
        else:
            return [True, []]

    def set_joint_range(self, joint1_range, joint2_range, joint3_range, joint4_range, joint5_range):
        # 设置关节范围
        set_joint_range(joint1_range, joint2_range, joint3_range, joint4_range, joint5_range, 'deg')
        fk.set_joint_range(joint1_range, joint2_range, joint3_range, joint4_range, joint5_range, 'deg')

    def get_joint_range(self):
        # 获取各个关节范围
        # joint1(min, max), joint2, joint3, joint4, joint5
        data = get_joint_range('deg')
        data1 = fk.get_joint_range('deg')
        if data == data1:
            return [True, data]
        else:
            reutrn [True, []]

    def set_joint_value_target(self, joint1, joint2, joint3, joint4, joint5):
        # 正运动学解
        '''
        给定每个舵机的转动角度，返回机械臂到达的目标位置姿态
        joint_value: 每个舵机转动的角度，列表形式[joint1, joint2, joint3, joint4, joint5]，单位脉宽
        return: 目标位置的3D坐标和位姿，格式geometry_msgs/Pose
        '''
        angle = transform.pulse2angle([joint1, joint2, joint3, joint4, joint5])
        res = fk.get_fk(angle)
        if res:
            return [True, True, res]
        else:
            return [True, False, []]
    
    def get_current_pose(self):
        # 获取机械臂当前位置
        res = fk.get_fk(angle)
        if res:
            return [True, True, res]
        else:
            return [True, False, []]

    def get_servo_position(self):
        # 获取舵机当前角度
        servo_positions = []
        for i in range(6):
            servo_positions.append(self.board.bus_servo_read_position(i + 1, True))
        return np.array(servo_positions[1:][::-1]) 
        # print(self.current_servo_positions)

    def set_ik(self, position, pitch, pitch_range=[-180, 180], roll=0.0, resolution=1):
        all_solutions = get_ik(position, pitch, pitch_range, roll, resolution)
        return all_solutions

    def set_pose_target(self, position, pitch, pitch_range=[-180, 180], roll=0.0, resolution=1):
        # 逆运动学解，获取最优解(所有电机转动最小)
        '''
        给定坐标和俯仰角，返回逆运动学解
        position: 目标位置，列表形式[x, y, z]，单位m
        roll: 目标俯仰角，单位度，范围-270~90
        roll_range: 如果在目标俯仰角找不到解，则在这个范围内寻找解
        resolution: roll_range范围角度的分辨率
        return: 调用是否成功， 舵机的目标位置， 当前舵机的位置， 机械臂的目标姿态， 最优解所有舵机转动的变化量
        '''
        position = list(position)

        # t1 = rospy.get_time()
        all_solutions = get_ik(position, pitch, list(pitch_range), roll, resolution)
        # t2 = rospy.get_time()
        # print(t2 - t1)
        current_servo_positions = self.get_servo_position()
        # print(current_servo_positions, all_solutions)
        if len(all_solutions) and len(current_servo_positions):
            rpy = []
            min_d = 1000*5
            optimal_solution = []
            for s in all_solutions:
                pulse_solutions = transform.angle2pulse(s[0], True)
                try:
                    for i in pulse_solutions:
                        d = np.array(i) - current_servo_positions
                        d_abs = np.maximum(d, -d)
                        min_sum = np.sum(d_abs)
                        if min_sum < min_d:
                            min_d = min_sum
                            for k in range(len(i)):
                                if i[k] < 0:
                                    i[k] = 0
                                elif i[k] > 1000:
                                    i[k] = 1000
                            rpy = s[1]
                            optimal_solution = i
                except BaseException as e:
                    print('choose solution error', e)
                    #print(pulse_solutions, current_servo_positions)
                # print(rospy.get_time() - t2)
            return [True, optimal_solution, current_servo_positions.tolist(), rpy, min_d]
        else:
            return [True, [], [], [], 0]

    def go_pose_target(self, position, pitch, pitch_range=[-180, 180], roll=0.0, use_time=0, resolution=1):
        res = self.set_pose_target(position, pitch, pitch_range, roll, resolution)
        if res[1]:
            self.board.bus_servo_set_position(use_time, [[2, res[1][4]], [3, res[1][3]], [4, res[1][2]], [5, res[1][1]], [6, res[1][0]]])
            return True
        else:
            return False

