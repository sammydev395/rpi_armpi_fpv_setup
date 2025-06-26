#!/usr/bin/env python3
# encoding:utf-8
# 扩展板按键(expansion board key)
import time
import gpiod

try:
    key1_pin = 13
    key2_pin = 23
    chip = gpiod.chip("gpiochip4")
    
    key1 = chip.get_line(key1_pin)
    config = gpiod.line_request()
    config.consumer = "key1"
    config.request_type = gpiod.line_request.DIRECTION_INPUT
    config.flags = gpiod.line_request.FLAG_BIAS_PULL_UP
    key1.request(config)

    key2 = chip.get_line(key2_pin)
    config = gpiod.line_request()
    config.consumer = "key2"
    config.request_type = gpiod.line_request.DIRECTION_INPUT
    config.flags = gpiod.line_request.FLAG_BIAS_PULL_UP
    key2.request(config)
    while True:
        print('\rkey1: {} key2: {}'.format(key1.get_value(), key2.get_value()), end='', flush=True)  # 打印key状态(print key state)
        time.sleep(0.001)
    chip.close()
except:
    print('按键默认被hw_button_scan占用，需要先关闭服务')
    print('sudo systemctl stop hw_button_scan.service')
