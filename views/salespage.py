#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Feb 02, 2018 09:59:23 AM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

from . import salespage_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = New_Toplevel_1 (root)
    salespage_support.init(root, top)
    root.mainloop()

w = None
def create_New_Toplevel_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = New_Toplevel_1 (w)
    salespage_m_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class New_Toplevel_1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+479+210")
        top.title("New Toplevel 1")
        top.configure(background="#ffddcc")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.TFrame1 = ttk.Frame(top)
        self.TFrame1.place(relx=0.18, rely=0.11, relheight=0.34, relwidth=0.64)
        self.TFrame1.configure(relief=SUNKEN)
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(relief=SUNKEN)
        self.TFrame1.configure(width=385)

        self.barcode = Entry(self.TFrame1)
        self.barcode.place(relx=0.13, rely=0.13, relheight=0.19, relwidth=0.76)
        self.barcode.configure(background="white")
        self.barcode.configure(disabledforeground="#a3a3a3")
        self.barcode.configure(font="TkFixedFont")
        self.barcode.configure(foreground="#000000")
        self.barcode.configure(highlightbackground="#d9d9d9")
        self.barcode.configure(highlightcolor="black")
        self.barcode.configure(insertbackground="black")
        self.barcode.configure(selectbackground="#c4c4c4")
        self.barcode.configure(selectforeground="black")

        self.sell_btn = Button(self.TFrame1)
        self.sell_btn.place(relx=0.39, rely=0.65, height=24, width=79)
        self.sell_btn.configure(activebackground="#d9d9d9")
        self.sell_btn.configure(activeforeground="#000000")
        self.sell_btn.configure(background="#003d99")
        self.sell_btn.configure(disabledforeground="#a3a3a3")
        self.sell_btn.configure(foreground="#fff")
        self.sell_btn.configure(highlightbackground="#d9d9d9")
        self.sell_btn.configure(highlightcolor="black")
        self.sell_btn.configure(pady="0")
        self.sell_btn.configure(text='''Sell''')

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)



        self.sales_label = ttk.Label(top)
        self.sales_label.place(relx=0.44, rely=0.0, height=42, width=84)
        self.sales_label.configure(background="#ffddcc")
        self.sales_label.configure(foreground="#000000")
        self.sales_label.configure(font="bold 25")
        self.sales_label.configure(relief=FLAT)
        self.sales_label.configure(anchor=CENTER)
        self.sales_label.configure(text='''Sales''')

        self.addItem = Button(top)
        self.addItem.place(relx=0.2, rely=0.73, height=44, width=117)
        self.addItem.configure(activebackground="#d9d9d9")
        self.addItem.configure(activeforeground="#000000")
        self.addItem.configure(background="#00802b")
        self.addItem.configure(disabledforeground="#a3a3a3")
        self.addItem.configure(foreground="#fff")
        self.addItem.configure(highlightbackground="#d9d9d9")
        self.addItem.configure(highlightcolor="black")
        self.addItem.configure(pady="0")
        self.addItem.configure(text='''Add Item''')

        self.reports_btn = Button(top)
        self.reports_btn.place(relx=0.63, rely=0.73, height=44, width=107)
        self.reports_btn.configure(activebackground="#d9d9d9")
        self.reports_btn.configure(activeforeground="#000000")
        self.reports_btn.configure(background="#005c99")
        self.reports_btn.configure(disabledforeground="#a3a3a3")
        self.reports_btn.configure(foreground="#fff")
        self.reports_btn.configure(highlightbackground="#d9d9d9")
        self.reports_btn.configure(highlightcolor="black")
        self.reports_btn.configure(pady="0")
        self.reports_btn.configure(text='''Reports''')
        self.barcode.focus()

if __name__ == '__main__':
    vp_start_gui()
