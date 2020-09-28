#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stop_lock_screen.py
@Time    :   2020/09/19 13:37:48
@Author  :   GuanYu 
@Version :   1.1
@Contact :   331423
'''

import os
import threading
import time
from tkinter import *

from check_mouse import check_mouse_move, text1

set_time = 15  # Set time of lockscreen
path = os.path.dirname(os.path.abspath(__file__))
top = Tk()
img1 = PhotoImage(file=os.path.join(path, "image\lock.png"))
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
        time.sleep(3)
        lab.config(text=text1[0])
        lab.update()


top.after(1000, show)
try:
    t = threading.Thread(target=check_mouse_move, args=(set_time, ))
    t.start()
    mainloop()
except:
    pass
