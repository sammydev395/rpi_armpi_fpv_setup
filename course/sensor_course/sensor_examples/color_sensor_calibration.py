#!/usr/bin/env python3
# coding=utf8
# 颜色传感器校准(color sensor calibration)
from sensor.apds9960 import APDS9960
from common.yaml_handle import save_yaml_data

#颜色传感器初始化(color sensor initialization)
apds = APDS9960()
apds.enableLightSensor()
count = 0
calib_color = None
data = {}
while True:
    #读取三个颜色通道值(read three color channel values)
    red = apds.readRedLight()
    green = apds.readGreenLight()
    blue = apds.readBlueLight()
    if calib_color == 'white':
        count += 1
        if count > 10:
            count = 0
            data['R_W'] = red
            data['G_W'] = green
            data['B_W'] = blue
            save_yaml_data(data, 'color_sensor_calibration.yaml') 
            calib_color = None
            print('white校准完成', red, green, blue)
    elif calib_color == 'black':
        count += 1
        if count > 10:
            count = 0
            data['R_B'] = red
            data['G_B'] = green
            data['B_B'] = blue
            save_yaml_data(data, 'color_sensor_calibration.yaml') 
            calib_color = None
            print('black校准完成', red, green, blue)
    else:
        calib_color = input('请输入要校准的颜色(white or black):')
    
