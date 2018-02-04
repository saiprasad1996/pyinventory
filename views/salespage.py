from tkinter import *
from tkinter import messagebox

from . import salespage_support
import views.Reports
from tkinter import messagebox
from backend.models import InventoryDB, Sales
from backend.utils import send_mail
import datetime
import os

class SalesPage:

    def toReport(self):
        views.Reports.create_New_Toplevel_1(top)

    def toAddItem(self):
        views.additem.create_Add_Item(top)

    def __init__(self):
        global top
        top = Tk()


        top.title("Kakaboka")
        C = Canvas(top, bg="blue", height=450, width=640)

        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'background.png')
        background_image = PhotoImage(file=image_path)


        background_label = Label(top, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.barcode_text = StringVar()
        self.quantity_ = IntVar()

        barcode_lbl = Label(background_label)
        barcode_lbl.place(relx=0.13, rely=0.16, height=31, width=59)
        # barcode_lbl.configure(background="#ffddcc")
        barcode_lbl.configure(disabledforeground="#a3a3a3")
        barcode_lbl.configure(foreground="#000000")
        barcode_lbl.configure(text='''Barcode''')
        barcode_lbl.configure(width=59)

        self.barcode = Entry(background_label)
        self.barcode.place(relx=0.25, rely=0.16, relheight=0.07, relwidth=0.46)
        # barcode.configure(background="white")
        self.barcode.configure(disabledforeground="#a3a3a3")
        self.barcode.configure(font="TkFixedFont")
        self.barcode.configure(foreground="#000000")
        self.barcode.configure(highlightbackground="#d9d9d9")
        self.barcode.configure(highlightcolor="black")
        self.barcode.configure(insertbackground="black")
        self.barcode.configure(selectbackground="#c4c4c4")
        self.barcode.configure(selectforeground="black")
        self.barcode.configure(textvariable=self.barcode_text)

        self.sell_btn = Button(background_label)
        self.sell_btn.place(relx=0.73, rely=0.16, height=34, width=87)
        self.sell_btn.configure(activebackground="#d9d9d9")
        self.sell_btn.configure(activeforeground="#000000")
        self.sell_btn.configure(background="#f9f9fa")
        self.sell_btn.configure(disabledforeground="#a3a3a3")
        self.sell_btn.configure(foreground="#000")
        self.sell_btn.configure(highlightbackground="#d9d9d9")
        self.sell_btn.configure(highlightcolor="black")
        self.sell_btn.configure(pady="0")
        self.sell_btn.configure(text='''Sell''')
        self.sell_btn.configure(command=self.sell)



        sales_label = Label(background_label)
        sales_label.place(relx=0.02, rely=0.0, height=63, width=202)
        sales_label.configure(font="bold 25")

        sales_label.configure(text='''KAKABOKA''')

        addItem = Button(background_label)
        addItem.place(relx=0.17, rely=0.62, height=44, width=117)
        addItem.configure(activebackground="#d9d9d9")
        addItem.configure(activeforeground="#000000")
        addItem.configure(background="#f9f9fa")
        addItem.configure(disabledforeground="#a3a3a3")
        addItem.configure(foreground="#000")
        addItem.configure(highlightbackground="#d9d9d9")
        addItem.configure(highlightcolor="black")
        addItem.configure(pady="0")
        addItem.configure(command=views.additem.vp_start_gui)
        addItem.configure(text='''Add Item''')

        reports_btn = Button(background_label)
        reports_btn.place(relx=0.63, rely=0.62, height=44, width=107)
        reports_btn.configure(activebackground="#d9d9d9")
        reports_btn.configure(activeforeground="#000000")
        reports_btn.configure(background="#f9f9fa")
        reports_btn.configure(disabledforeground="#a3a3a3")
        reports_btn.configure(foreground="#000")
        reports_btn.configure(highlightbackground="#d9d9d9")
        reports_btn.configure(highlightcolor="black")
        reports_btn.configure(pady="0")
        reports_btn.configure(text='''Reports''')
        reports_btn.configure(command=self.toReport)
        self.barcode.focus()

        Label2 = Label(background_label)
        Label2.place(relx=0.13, rely=0.31, height=21, width=52)
        # Label2.configure(background="#ffddcc")
        Label2.configure(disabledforeground="#a3a3a3")
        Label2.configure(foreground="#000000")
        Label2.configure(text='''Quantity''')

        quantity = Entry(background_label)
        quantity.place(relx=0.25, rely=0.31, relheight=0.07, relwidth=0.46)

        quantity.configure(font="TkFixedFont")

        quantity.configure(insertbackground="black")
        quantity.configure(textvariable=self.quantity_)
        quantity.insert(END, 1)
        quantity.configure(width=234)
        C.pack()
        top.mainloop()


    def sell(self):
        try:
            # print("Sell called")

            barcodetext = str(self.barcode_text.get())
            quantity_ = int(self.quantity_.get())
            # print(quantity_)
            sellable = InventoryDB()
            sellable = sellable.getInventoryRecodeByBarcode(barcodetext)
            # print(sellable)
            sellable = sellable[0]
            if (sellable.quantity > quantity_):
                sellable.quantity = sellable.quantity - quantity_
                saved = sellable.save(update=True)
                sold_price = sellable.price * quantity_
                sell = Sales(barcode=barcodetext, time=str(datetime.datetime.now()), quantity=quantity_,
                             itemname=sellable.itemname, amount=sold_price)
                sold = sell.save(insert=True)
                if saved == 1 and sold == 1:
                    messagebox.showinfo(title="Success", message="Sold successfully")
                    self.barcode.delete(0, END)
                else:
                    messagebox.showinfo(title="Failed", message="Could not sell {}".format(self.barcode_text.get()))
            elif sellable.quantity == 0:
                send_mail(subject="Stock Update",
                                message="The stock for {} is finished up. Please add some stock to the inventory".format(
                                    sellable.itemname))
                messagebox.showinfo(title="Oops..",message="The stock is empty. A Remainder mail is sent to you")
            else:
                messagebox.showinfo(title="Sorry :(",
                                    message="Stock not available. The available qunatity is {} ".format(
                                        sellable.quantity))
        except IndexError:
            messagebox.showinfo(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.get()))
        except TypeError:
            messagebox.showinfo(title="Failed", message="Barcode not provided")

# SalesPage()



# #! /usr/bin/env python
# #
# # GUI module generated by PAGE version 4.9
# # In conjunction with Tcl version 8.6
# #    Feb 02, 2018 09:59:23 AM
# import sys
#
# try:
#     from Tkinter import *
# except ImportError:
#     from tkinter import *
#
# try:
#     import ttk
#
#     py3 = 0
# except ImportError:
#     import tkinter.ttk as ttk
#
#     py3 = 1
#
# from . import salespage_support
# import views.Reports
# from tkinter import messagebox
# from backend.models import InventoryDB, Sales
# from backend.utils import send_mail
# import datetime
#
#
# def vp_start_gui():
#     '''Starting point when module is the main routine.'''
#     global val, w, root
#     root = Tk()
#     top = New_Toplevel_1(root)
#     salespage_support.init(root, top)
#     root.mainloop()
#
#
# w = None
#
#
# def create_New_Toplevel_1(root, *args, **kwargs):
#     '''Starting point when module is imported by another program.'''
#     global w, w_win, rt
#     rt = root
#     w = Toplevel(root)
#     top = New_Toplevel_1(w)
#     salespage_support.init(w, top, *args, **kwargs)
#     return (w, top)
#
#
# def destroy_New_Toplevel_1():
#     global w
#     w.destroy()
#     w = None
#
#
# class New_Toplevel_1:
#     def toReport(self):
#         views.Reports.create_New_Toplevel_1(w)
#
#     def toAddItem(self):
#         views.additem.create_Add_Item(w)
#
#     def sell(self):
#         try:
#             # print("Sell called")
#
#             barcodetext = str(self.barcode_text.get())
#             quantity_ = int(self.quantity_.get())
#             # print(quantity_)
#             sellable = InventoryDB()
#             sellable = sellable.getInventoryRecodeByBarcode(barcodetext)
#             # print(sellable)
#             sellable = sellable[0]
#             if (sellable.quantity > quantity_):
#                 sellable.quantity = sellable.quantity - quantity_
#                 saved = sellable.save(update=True)
#                 sold_price = sellable.price * quantity_
#                 sell = Sales(barcode=barcodetext, time=str(datetime.datetime.now()), quantity=quantity_,
#                              itemname=sellable.itemname, amount=sold_price)
#                 sold = sell.save(insert=True)
#                 if saved == 1 and sold == 1:
#                     messagebox.showinfo(title="Success", message="Sold successfully")
#                     self.barcode.delete(0, END)
#                 else:
#                     messagebox.showinfo(title="Failed", message="Could not sell {}".format(self.barcode_text.get()))
#             elif sellable.quantity == 0:
#                 send_mail(subject="Stock Update",
#                                 message="The stock for {} is finished up. Please add some stock to the inventory".format(
#                                     sellable.itemname))
#                 messagebox.showinfo(title="Oops..",message="The stock is empty. A Remainder mail is sent to you")
#             else:
#                 messagebox.showinfo(title="Sorry :(",
#                                     message="Stock not available. The available qunatity is {} ".format(
#                                         sellable.quantity))
#         except IndexError:
#             messagebox.showinfo(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.get()))
#         except TypeError:
#             messagebox.showinfo(title="Failed", message="Barcode not provided")

#     def __init__(self, top=None):
#         '''This class configures and populates the toplevel window.
#            top is the toplevel containing window.'''
#
#         import os
#         base_folder = os.path.dirname(__file__)
#         C = Canvas(top, bg="blue", height=450, width=640)
#
        # image_path = os.path.join(base_folder, 'background.png')
        # background_image = PhotoImage(file=image_path)
        # background_label = Label(top, image=background_image)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
#         # background_label.pack()
#         C.pack()
#
#
#         # _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
#         # _fgcolor = '#000000'  # X11 color: 'black'
#         # _compcolor = '#d9d9d9'  # X11 color: 'gray85'
#         # _ana1color = '#d9d9d9'  # X11 color: 'gray85'
#         # _ana2color = '#d9d9d9'  # X11 color: 'gray85'
#         # self.style = ttk.Style()
#         # if sys.platform == "win32":
#         #     self.style.theme_use('winnative')
#         # # self.style.configure('.',background=_bgcolor)
#         # self.style.configure('.', background=background_label)
#         # self.style.configure('.', foreground=_fgcolor)
#         # self.style.configure('.', font="TkDefaultFont")
#         # self.style.map('.', background=
#         # [('selected', _compcolor), ('active', _ana2color)])
#
#         top.geometry("600x450+479+210")
#         top.title("Sales")
#         top.configure(background="#ffddcc")
#         top.configure(highlightbackground="#d9d9d9")
#         top.configure(highlightcolor="black")
#
#         self.barcode_text = StringVar()
#         self.quantity_ = IntVar()
#
#         self.barcode_lbl = Label(background_label)
#         self.barcode_lbl.place(relx=0.13, rely=0.16, height=31, width=59)
#         # self.barcode_lbl.configure(background="#ffddcc")
#         self.barcode_lbl.configure(disabledforeground="#a3a3a3")
#         self.barcode_lbl.configure(foreground="#000000")
#         self.barcode_lbl.configure(text='''Barcode''')
#         self.barcode_lbl.configure(width=59)
#
#         self.barcode = Entry(background_label)
#         self.barcode.place(relx=0.25, rely=0.16, relheight=0.07, relwidth=0.46)
#         # self.barcode.configure(background="white")
#         self.barcode.configure(disabledforeground="#a3a3a3")
#         self.barcode.configure(font="TkFixedFont")
#         self.barcode.configure(foreground="#000000")
#         self.barcode.configure(highlightbackground="#d9d9d9")
#         self.barcode.configure(highlightcolor="black")
#         self.barcode.configure(insertbackground="black")
#         self.barcode.configure(selectbackground="#c4c4c4")
#         self.barcode.configure(selectforeground="black")
#         self.barcode.configure(textvariable=self.barcode_text)
#
#         self.sell_btn = Button(background_label)
#         self.sell_btn.place(relx=0.73, rely=0.16, height=34, width=87)
#         self.sell_btn.configure(activebackground="#d9d9d9")
#         self.sell_btn.configure(activeforeground="#000000")
#         self.sell_btn.configure(background="#003d99")
#         self.sell_btn.configure(disabledforeground="#a3a3a3")
#         self.sell_btn.configure(foreground="#fff")
#         self.sell_btn.configure(highlightbackground="#d9d9d9")
#         self.sell_btn.configure(highlightcolor="black")
#         self.sell_btn.configure(pady="0")
#         self.sell_btn.configure(text='''Sell''')
#         self.sell_btn.configure(command=self.sell)
#
#
#
#         self.sales_label = Label(background_label)
#         self.sales_label.place(relx=0.02, rely=0.0, height=63, width=202)
#         # self.sales_label.configure(background="#ffddcc")
#         self.sales_label.configure(disabledforeground="#a3a3a3")
#         self.sales_label.configure(font="bold 25")
#         self.sales_label.configure(foreground="#000000")
#         self.sales_label.configure(text='''KAKABOKA''')
#
#         self.addItem = Button(background_label)
#         self.addItem.place(relx=0.17, rely=0.62, height=44, width=117)
#         self.addItem.configure(activebackground="#d9d9d9")
#         self.addItem.configure(activeforeground="#000000")
#         self.addItem.configure(background="#00802b")
#         self.addItem.configure(disabledforeground="#a3a3a3")
#         self.addItem.configure(foreground="#fff")
#         self.addItem.configure(highlightbackground="#d9d9d9")
#         self.addItem.configure(highlightcolor="black")
#         self.addItem.configure(pady="0")
#         self.addItem.configure(command=self.toAddItem)
#         self.addItem.configure(text='''Add Item''')
#
#         self.reports_btn = Button(background_label)
#         self.reports_btn.place(relx=0.63, rely=0.62, height=44, width=107)
#         self.reports_btn.configure(activebackground="#d9d9d9")
#         self.reports_btn.configure(activeforeground="#000000")
#         self.reports_btn.configure(background="#005c99")
#         self.reports_btn.configure(disabledforeground="#a3a3a3")
#         self.reports_btn.configure(foreground="#fff")
#         self.reports_btn.configure(highlightbackground="#d9d9d9")
#         self.reports_btn.configure(highlightcolor="black")
#         self.reports_btn.configure(pady="0")
#         self.reports_btn.configure(text='''Reports''')
#         self.reports_btn.configure(command=self.toReport)
#         self.barcode.focus()
#
#         self.Label2 = Label(background_label)
#         self.Label2.place(relx=0.13, rely=0.31, height=21, width=52)
#         # self.Label2.configure(background="#ffddcc")
#         self.Label2.configure(disabledforeground="#a3a3a3")
#         self.Label2.configure(foreground="#000000")
#         self.Label2.configure(text='''Quantity''')
#
#         self.quantity = Entry(background_label)
#         self.quantity.place(relx=0.25, rely=0.31, relheight=0.07, relwidth=0.46)
#         self.quantity.configure(background="white")
#         self.quantity.configure(disabledforeground="#a3a3a3")
#         self.quantity.configure(font="TkFixedFont")
#         self.quantity.configure(foreground="#000000")
#         self.quantity.configure(insertbackground="black")
#         self.quantity.configure(textvariable=self.quantity_)
#         self.quantity.insert(END, 1)
#         self.quantity.configure(width=234)
#
#
# if __name__ == '__main__':
#     vp_start_gui()
