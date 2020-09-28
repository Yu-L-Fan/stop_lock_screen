#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stop_lockScreen.py
@Time    :   2020/09/18 19:15:04
@Author  :   GuanYu 
@Version :   1.0
@Contact :   331423
'''


import time
from pynput import keyboard, mouse

def check_mouse_move(t):
    my_mouse = mouse.Controller()
    my_keyboard = keyboard.Controller()
    old_pos = my_mouse.position
    start_time = time.time()
    i = 1
    while True:
        time.sleep(60)
        try:
            if abs(my_mouse.position[0] -
                   old_pos[0]) + abs(my_mouse.position[1] - old_pos[1]) >= 5:
                start_time = time.time()
                old_pos = my_mouse.position
                print(str('%04d' %i) + '\t' + 'time reset...')
                i += 1
            elif time.time() - start_time <= (t - 2) * 60:
                my_keyboard.press(keyboard.Key.print_screen)
                time.sleep(0.01)
                my_keyboard.release(keyboard.Key.print_screen)
            else:
                text = 'Screen will be loced soon...'
                continue
        except:
            continue


if __name__ == "__main__":
    print('start...')
    check_mouse_move(20)
