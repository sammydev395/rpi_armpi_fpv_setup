#!/usr/bin/env python3
# encoding: utf-8
import os
import time
import sqlite3 as sql

class ActionGroupController:
    runningAction = False
    stopRunning = False

    def __init__(self, board, action_path=os.path.split(os.path.realpath(__file__))[0]):
        self.action_path = action_path
        self.board = board

    def stop_servo(self):
        self.board.bus_servo_stop([1, 2, 3, 4, 5, 6]) 
            
    def stop_action_group(self):
        self.stopRunning = True

    def runAction(self, actNum):        
        if actNum is None:
            return
        actNum = os.path.join(self.action_path, actNum + ".d6a")
        self.stopRunning = False
        if os.path.exists(actNum) is True:
            if self.runningAction is False:
                self.runningAction = True
                ag = sql.connect(actNum)
                cu = ag.cursor()
                cu.execute("select * from ActionGroup")
                while True:
                    act = cu.fetchone()
                    if self.stopRunning is True:
                        self.stopRunning = False                   
                        break
                    if act is not None:
                        data = []
                        for i in range(0, len(act)-2, 1):
                            data.extend([[i + 1, act[2 + i]]])
                        self.board.bus_servo_set_position(float(act[1])/1000.0, data)
                        time.sleep(float(act[1])/1000.0)
                    else:
                        break
                self.runningAction = False
                
                cu.close()
                ag.close()
        else:
            self.runningAction = False

