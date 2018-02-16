from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk

from . import salespage_support
import views.Reports
from tkinter import messagebox
from backend.models import InventoryDB, Sales
from backend.utils import send_mail
from backend.database import *
import views.categories
import datetime
import os
import json

class SalesPage:
    def toReport(self):
        views.Reports.create_New_Toplevel_1(top)

    def toAddItem(self):
        views.categories.create_Categories(top)

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

        menu = Menu(top)
        top.config(menu=menu)

        fileSubmenu = Menu(menu)
        menu.add_cascade(label="Program", menu=fileSubmenu)
        fileSubmenu.add_command(label="Setup database",command=self.setupDatabase)
        # fileSubmenu.add_command(label="New..")
        fileSubmenu.add_separator()
        fileSubmenu.add_command(label="Exit",command=top.destroy)

        # editMenu = Menu(menu)
        # menu.add_cascade(label="Edit", menu=editMenu)
        # editMenu.add_command(label="Redo")

        barcode_lbl = ttk.Label(background_label)
        barcode_lbl.place(relx=0.13, rely=0.16, height=31, width=59)
        # barcode_lbl.configure(background="#ffddcc")
        # barcode_lbl.configure(disabledforeground="#a3a3a3")
        # barcode_lbl.configure(foreground="#000000")
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

        self.barcode.bind("<Return>", self.sell_key)

        self.sell_btn = ttk.Button(background_label)
        self.sell_btn.place(relx=0.73, rely=0.16, height=34, width=87)
        # self.sell_btn.configure(activebackground="#d9d9d9")
        # self.sell_btn.configure(activeforeground="#000000")
        # self.sell_btn.configure(background="#f9f9fa")
        # self.sell_btn.configure(disabledforeground="#a3a3a3")
        # self.sell_btn.configure(foreground="#000")
        # self.sell_btn.configure(highlightbackground="#d9d9d9")
        # self.sell_btn.configure(highlightcolor="black")
        # self.sell_btn.configure(pady="0")
        self.sell_btn.configure(text='''Sell''')
        self.sell_btn.configure(command=self.sell)

        sales_label = Label(background_label)
        sales_label.place(relx=0.02, rely=0.0, height=63, width=202)
        sales_label.configure(font="bold 25")

        sales_label.configure(text='''KAKABOKA''')

        addItem = ttk.Button(background_label)
        addItem.place(relx=0.17, rely=0.62, height=44, width=117)
        # addItem.configure(activebackground="#d9d9d9")
        # addItem.configure(activeforeground="#000000")
        # addItem.configure(background="#f9f9fa")
        # addItem.configure(disabledforeground="#a3a3a3")
        # addItem.configure(foreground="#000")
        # addItem.configure(highlightbackground="#d9d9d9")
        # addItem.configure(highlightcolor="black")
        # addItem.configure(pady="0")
        addItem.configure(command=self.toAddItem)
        addItem.configure(text='''Add Item''')

        reports_btn = ttk.Button(background_label)
        reports_btn.place(relx=0.63, rely=0.62, height=44, width=107)
        # reports_btn.configure(activebackground="#d9d9d9")
        # reports_btn.configure(activeforeground="#000000")
        # reports_btn.configure(background="#f9f9fa")
        # reports_btn.configure(disabledforeground="#a3a3a3")
        # reports_btn.configure(foreground="#000")
        # reports_btn.configure(highlightbackground="#d9d9d9")
        # reports_btn.configure(highlightcolor="black")
        # reports_btn.configure(pady="0")
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

    def sell_key(self, event):
        self.sell()

    def setupDatabase(self):
        report = setupDatabase()
        if report == {}:

            messagebox.showinfo("Info","Database is already setup")
        else:
            messagebox.showinfo("Info",json.dumps(report))

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
                    messagebox.showinfo(title="Success",
                                        message="Item {} of quantity {} sold successfully".format(sellable.itemname,
                                                                                                  quantity_))
                    self.barcode.delete(0, END)
                else:
                    messagebox.showinfo(title="Failed", message="Could not sell {}".format(self.barcode_text.get()))
            elif sellable.quantity == 0:
                send_mail(subject="Stock Update",
                          message="The stock for {} is finished up. Please add some stock to the inventory".format(
                              sellable.itemname))
                messagebox.showinfo(title="Oops..", message="The stock is empty. A Remainder mail is sent to you")
            else:
                messagebox.showinfo(title="Sorry :(",
                                    message="Stock not available. The available qunatity is {} ".format(
                                        sellable.quantity))
        except IndexError:
            messagebox.showinfo(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.get()))
        except TypeError:
            messagebox.showinfo(title="Failed", message="Barcode not provided")
