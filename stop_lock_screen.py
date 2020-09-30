#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stop_lock_screen.py
@Time    :   2020/09/19 13:37:48
@Author  :   GuanYu 
@Version :   1.2
@Contact :   331423
@Des     :   单文件脚本，文件包含my_exe.bat、lock.png、stop_lock_screen.py，三个文件，将my_exe.bat放入开机启动文件夹可实现开机自动执行。
'''

import os
import threading
import time
from tkinter import *

from pynput import keyboard, mouse


def check_mouse_move(t):
    global text1
    my_mouse = mouse.Controller()
    my_keyboard = keyboard.Controller()
    old_pos = my_mouse.position
    start_time = time.time()
    while True:
        time.sleep(1)
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


text1 = [' Running.....']
set_time = 15  # Set time of lockscreen
path = os.path.dirname(os.path.abspath(__file__))

top = Tk()
img1 = PhotoImage(file=os.path.join(path, "lock.png"))
lab = Label(top,
            text=text1[0],
            image=img1,
            compound="left",
            font=('Consolas', '12'),
            fg='white',
            bg='black')
lab.master.overrideredirect(True)
lab.master.geometry("+1785+1010")
lab.pack()


def show():
    while True:
        time.sleep(0.3)
        lab.config(text=text1[0])
        lab.update()


top.after(1000, show)
try:
    t = threading.Thread(target=check_mouse_move, args=(set_time, ))
    t.start()
    mainloop()
except:
    pass
