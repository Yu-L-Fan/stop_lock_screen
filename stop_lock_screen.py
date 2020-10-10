#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stop_lock_screen.py
@Time    :   2020/09/19 13:37:48
@Author  :   GuanYu 
@Version :   1.5
@Contact :   331423
@Des     :   单文件脚本，文件包含my_exe.bat、lock.png、stop_lock_screen.py，
             三个文件，将my_exe.bat放入开机启动文件夹可实现开机自动执行。
             
             + 实现右键弹出退出菜单，可正常结束脚本
             + 更改按键为scroll_lock，避免剪贴板覆盖截屏
             + 监测Scroll Lock是否已经激活，避免激活该按键
'''

import ctypes
import inspect
import os
import threading
import time
from tkinter import *
from tkinter import messagebox
from win32api import GetKeyState
from win32con import VK_SCROLL

from pynput import keyboard, mouse


def _async_raise(tid, exctype):
    """ Function of killing thread """
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    """ Function of killing thread """
    _async_raise(thread.ident, SystemExit)


def press_key(my_keyboard):
    """ Function of pressing key """
    s = 1 if GetKeyState(VK_SCROLL) else 2 # if scroll_lock has been activitied,just press one time,else twice.
    for i in range(s):
        my_keyboard.press(keyboard.Key.scroll_lock)
        time.sleep(0.1)
        my_keyboard.release(keyboard.Key.scroll_lock)


def check_mouse_move(t):
    """ Check mouse's movement,and press the key to prevent lock screen,
        and update text. """
    global text1, press_fre
    my_mouse = mouse.Controller()
    my_keyboard = keyboard.Controller()
    old_pos = my_mouse.position
    start_time = time.time()
    press_time = time.time()
    while True:
        time.sleep(check_fre)
        try:
            if abs(my_mouse.position[0] -
                   old_pos[0]) + abs(my_mouse.position[1] - old_pos[1]) >= 10:
                start_time = time.time()
                old_pos = my_mouse.position
                text1[0] = ' Running.....'
            elif time.time() - start_time <= (t - 2) * 60:
                if time.time() - press_time > press_fre:
                    press_key(my_keyboard)
                    press_time = time.time()
                text1[0] = ' Running.....'
            else:
                text1[0] = ' Lock soon...'
                continue
        except:
            continue


def quit_menu(event):
    """ Quit menu,triggered by clicking on text window with right mouse button  """
    global flag
    flag = not (messagebox.askokcancel("退出", "确定退出吗？"))
    # but1 = Button(top, text="Quit", width=10, height=2, command=top.quit)
    # but1.pack()


def show():
    """ Update status witn text on screen,and monitoring exit behavior"""
    global t1, top, flag
    while flag:
        try:
            time.sleep(display_fre)
            lab.config(text=text1[0])
            lab.update()
        except Exception as e:
            break
    stop_thread(t1)
    top.destroy()


flag = True
text1 = [' Running.....']
set_time = 20  # Set screen lock time/min
display_fre = 0.3  # Show refresh interval/s
check_fre = 1  # Set check time frequency/s
press_fre = 30  # Set press time frequency/s
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
lab.master.geometry("+1780+1015")
lab.pack()

top.after(1000, show)
top.bind('<Button-3>', quit_menu)
try:
    t1 = threading.Thread(target=check_mouse_move, args=(set_time, ))
    t1.start()
    mainloop()
except:
    pass
