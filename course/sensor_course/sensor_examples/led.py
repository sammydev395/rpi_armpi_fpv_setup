#!/usr/bin/env python3
# encoding:utf-8
# 扩展板led(expansion board led)
import time
import gpiod

try:
    print('led闪烁: 0.1/s')
    led1_pin = 16  # 蓝色led(blue led)
    led2_pin = 26 
    chip = gpiod.chip('gpiochip4')

    led1 = chip.get_line(led1_pin)
    config = gpiod.line_request()
    config.consumer="led1"
    config.request_type=gpiod.line_request.DIRECTION_OUTPUT
    led1.request(config)

    led2 = chip.get_line(led2_pin)
    config = gpiod.line_request()
    config.consumer="led2"
    config.request_type=gpiod.line_request.DIRECTION_OUTPUT
    led2.request(config)

    while True:
        led1.set_value(0)
        time.sleep(0.1)
        led1.set_value(1)
        led2.set_value(0)
        time.sleep(0.1)
        led2.set_value(1)
except:
    print('led默认被hw_wifi占用，需要自行注释掉相关代码')
    print('然后重启服务sudo systemctl restart hw_wifi.service')
