from tkinter import *
from tkinter.messagebox import *
from tkinter.font import *
import operator
import os

window = Tk()
window.title("哔哩哔哩视频数据分析")
window.geometry("700x350+250+150")



#菜单栏
def aboutCall():
    showinfo(title = "关于",message = "独立完成人：余柏辰")
def helpCall():
    showinfo(title = "功能介绍", message = "输入任何一个b站视频地址(av号bv号均可)，进行数据分析并展示观众分布、评论态度与词云，旨在帮助用户对视频的影响有更深的认识。")
def whereCall():
    showinfo(title = "文件目录", message = os.getcwd())
menubar = Menu(window)
startmenu = Menu(menubar)
startmenu.add_command(label = "目录", command = whereCall)
startmenu.add_command(label = "退出", command = window.destroy)
menubar.add_cascade(label = "文件",menu = startmenu)
helpmenu = Menu(menubar)
helpmenu.add_command(label="About", command=aboutCall)
helpmenu.add_command(label="说明", command=helpCall)
menubar.add_cascade(label="帮助", menu=helpmenu)
window.config(menu=menubar)

#进入GUI
window.mainloop()
