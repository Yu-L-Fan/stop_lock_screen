#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   check_mouse.py
@Time    :   2020/09/15 14:51:48
@Author  :   GuanYu 
@Version :   1.0
@Contact :   331423
'''

import time
from pynput import mouse, keyboard

text1 = [' Running.....']


def check_mouse_move(t):
    global text1
    my_mouse = mouse.Controller()
    my_keyboard = keyboard.Controller()
    old_pos = my_mouse.position
    start_time = time.time()
    while True:
        time.sleep(10)
        try:
            if abs(my_mouse.position[0] -
                   old_pos[0]) + abs(my_mouse.position[1] - old_pos[1]) >= 10:
                start_time = time.time()
                old_pos = my_mouse.position
                text1[0] = ' Running.....'
            elif time.time() - start_time <= (t - 2) * 60:
                my_keyboard.press(keyboard.Key.print_screen)
                time.sleep(0.01)
                my_keyboard.release(keyboard.Key.print_screen)
                text1[0] = ' Running.....'
            else:
                text1[0] = ' Lock soon...'
                continue
        except:
            continue
