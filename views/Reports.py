#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jan 24, 2018 04:56:57 PM
import sys

from views.tables import createTable

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

from views import Reports_support, reportstable
from backend.models import *
from tkinter import messagebox


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    Reports_support.set_Tk_var()
    top = New_Toplevel_1(root)
    Reports_support.init(root, top)
    root.mainloop()


w = None


def create_New_Toplevel_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel(root)
    Reports_support.set_Tk_var()
    top = New_Toplevel_1(w)
    Reports_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class New_Toplevel_1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        # _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        # _fgcolor = '#000000'  # X11 color: 'black'
        # _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        # _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        # _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        # self.style = ttk.Style()
        # if sys.platform == "win32":
        #     self.style.theme_use('winnative')
        # self.style.configure('.', background=_bgcolor)
        # self.style.configure('.', foreground=_fgcolor)
        # self.style.configure('.', font="TkDefaultFont")
        # self.style.map('.', background=
        # [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("600x450+487+182")
        top.title("Reports")
        top.configure(background="#ffddcc")

        self.Label1 = Label(top)
        self.Label1.place(relx=0.4, rely=0.02, height=44, width=119)
        self.Label1.configure(background="#ffddcc")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="Bold 25")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Reports''')

        self.TCombobox1 = ttk.Combobox(top)
        self.TCombobox1.place(relx=0.2, rely=0.18, relheight=0.07, relwidth=0.36)
        value_list = ["Sales", "Stock"]
        self.TCombobox1.configure(values=value_list)
        self.TCombobox1.configure()
        self.TCombobox1.configure(textvariable=Reports_support.combobox)
        self.TCombobox1.configure(width=213)
        self.TCombobox1.configure(takefocus="")

        self.Button1 = Button(top)
        self.Button1.place(relx=0.63, rely=0.18, height=34, width=77)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#0052cc")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="Bold")
        self.Button1.configure(foreground="#fff")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Search''')
        self.Button1.configure(width=77)

        # self.tframe = Frame(top)

        # self.table = createTable(self.tframe, [["Sl No", "Name", "Price"], [1, "Shampoo", 20], [1, "Hair Color", 15]])
        # self.table.grid()
        # self.tframe.place(height=200,width=300)
        # self.tframe.pack()
        self.Button1.configure(command=self.renderTable)

    def renderTable(self):
        what = self.TCombobox1.get()
        datalist = [["Sl No", "Name", "Price"], [1, "Shampoo", 20], [1, "Hair Color", 15]]
        if str.lower(what) == str.lower("Stock"):
            datalist = InventoryDB()

            datalist = datalist.getInventory()
            items = [["Sl No", "Barcode", "Item Name", "Price", "Manufacturer", "Quantity","Category"]]
            for i in enumerate(datalist):
                items.append([ i[0]+1,i[1].barcode, i[1].itemname, i[1].price, i[1].manufacturer, i[1].quantity,i[1].category])

            reportstable.renderTable(items)

        elif str.lower(what) == str.lower("Sales"):
            datalist = InventoryDB()

            datalist = datalist.getAllSales()
            items = [["ID", "Barcode", "Item Name", "time", "Quantity", "Selling Amount"]]
            for i in datalist:
                items.append([i.id, i.barcode, i.itemname, i.time, i.quantity, i.amount])
            reportstable.renderTable(items)

        else:
            messagebox.showinfo("Info", "Please select a correct option to proceed")


if __name__ == '__main__':
    vp_start_gui()