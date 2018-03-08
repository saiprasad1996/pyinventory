import os
import smtplib

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from backend.utils import messagebox, generateInvoiceNumber
import json
from backend.models import InventoryDB, Sales, log
from backend.utils import send_mail
from backend.database import *
from backend import config
import datetime
import os
import json
from views import categories_kivy
from kivy.uix.screenmanager import Screen


class EmptyBasketError(Exception):
    pass


class SalesPageLayout(FloatLayout):
    title = 'KAKABOKA'
    basket = []

    def __init__(self):
        super(SalesPageLayout, self).__init__()
        # self.root = root = FloatLayout()
        root = self
        root.bind(size=self._update_rect, pos=self._update_rect)
        self.bar_str = ''
        self.qty_str = ''

        # barcode label
        label_qty = Label(text='Quantity',
                          color=(0, 0, 0, 0.25),
                          font_size=20,
                          pos_hint={'center_x': 0.175, 'center_y': 0.7})
        root.add_widget(label_qty)

        # label_selling = Label(text='Selling Price',
        #                   color=(0, 0, 0, 0.25),
        #                   font_size=20,
        #                   pos_hint={'center_x': 0.175, 'center_y': 0.6})
        # root.add_widget(label_selling)

        self.selling_price = TextInput(hint_text="Selling Price",
                                       size_hint=(0.2, 0.075),
                                       multiline=False,
                                       pos_hint={'center_x': 0.35, 'center_y': 0.6})

        root.add_widget(self.selling_price)

        # label_tip = Label(text='Tip',
        #                   color=(0, 0, 0, 0.25),
        #                   font_size=20,
        #                   pos_hint={'center_x': 0.175, 'center_y': 0.6})
        # root.add_widget(label_tip)

        # self.tip = TextInput(hint_text="Tip",
        #                      multiline=False,
        #                      size_hint=(0.2, 0.075),
        #                      pos_hint={'center_x': 0.63, 'center_y': 0.6})
        #
        # root.add_widget(self.tip)

        # quantity label
        label_bar = Label(text='Barcode',
                          color=(0, 0, 0, 0.25),
                          font_size=20,
                          pos_hint={'center_x': 0.175, 'center_y': 0.8})
        root.add_widget(label_bar)
        # text box for barcode
        self.barcode_text = TextInput(hint_text='barcode',
                                      multiline=False,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                      size_hint=(0.5, 0.075))

        def on_text(instance, value):
            # use try to check if value in database
            self.bar_str = self.barcode_text.text

        self.barcode_text.bind(text=on_text)
        root.add_widget(self.barcode_text)

        # text box for quantity
        self.quantity_ = TextInput(text='1',
                                   multiline=False,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                   size_hint=(0.5, 0.075))

        def on_text(instance, value):
            # use try to check if value in database
            self.qty_str = str(self.quantity_.text)

        self.quantity_.bind(text=on_text)
        root.add_widget(self.quantity_)

        # company name
        title_label = Label(text='KAKABOKA',
                            color=(0, 0, 0, 1),
                            font_size=30,
                            pos_hint={'center_x': 0.12, 'center_y': 0.95})
        root.add_widget(title_label)

        # Enter the barcode
        enter_btn = Button(text='Enter',
                           size_hint=(0.15, 0.1),
                           pos_hint={'right': 0.95, 'center_y': 0.8})

        def enter_btn_pressed(instance):
            try:
                # in response of the button click
                barcode_ = self.barcode_text.text
                quantity_text = int(self.quantity_.text)
                if len(barcode_) == 0:
                    messagebox(title='Warning', message="Please enter the barcode")
                    return
                else:
                    barcode_ = int(barcode_)
                    record = InventoryDB().getInventoryRecodeByBarcode(barcode=barcode_)
                    if len(record) == 0:
                        messagebox(title="Error", message="No such item with {} barcode exists".format(barcode_))
                        return
                    else:
                        record = record[0]
                        print(record.quantity >= quantity_text and record.category == "SERVICE")
                        if record.quantity >= quantity_text or record.category == "SERVICE":
                            total_price = float(record.price) * float(quantity_text)
                            obj = {"barcode": self.bar_str, "Item Name": record.itemname,
                                   "quantity": str(self.quantity_.text), "amount": total_price}
                            if len(self.selling_price.text) > 0:
                                if float(self.selling_price.text) != 0:
                                    obj["amount"] = float(self.selling_price.text) * float(quantity_text)

                            self.basket.append(obj)
                            # label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'
                            self.label1.text = self.label1.text + """ Barcode : {} | Item Name : {} | Quantity : {} | Amount : {}""".format(
                                obj["barcode"], obj["Item Name"], obj["quantity"], obj["amount"]) + "\n"
                            self.barcode_text.text = ""
                            self.quantity_.text = "1"

                        else:
                            # send_mail(subject="Stock Update",
                            #           message="The stock for {} is finished up. Please add some stock to the inventory".format(
                            #               record.itemname))
                            messagebox(title="Sorry :(",
                                       message="Stock not available. The available quantity is {} ".format(
                                           record.quantity))
            except TypeError:
                messagebox(title="Failed", message="Quantity must be a Numeric value")
            except ValueError:
                messagebox(title="Failed", message="Quantity must be a Numeric value")
            except smtplib.SMTPServerDisconnected:
                print("Internet Not connected")

        self.barcode_text.bind(on_text_validate=enter_btn_pressed)
        enter_btn.bind(on_press=enter_btn_pressed)
        root.add_widget(enter_btn)

        # To finish entry and get the final total.
        done_btn = Button(text='Done',
                          size_hint=(0.2, 0.15),
                          pos_hint={'center_x': 0.5, 'center_y': 0.2})

        # def callback2(instance):
        #     label1.text = label1.text + '\n Done'

        # done_btn.bind(on_press=self.sellAll)
        done_btn.bind(on_press=self.sellPopUp)
        root.add_widget(done_btn)

        # add item
        self.button_add = Button(text='+',
                                 size_hint=(0.15, 0.1),
                                 pos_hint={'right': 0.85 - 0.01, 'center_y': 0.075})
        # def callback1(instance):
        # in response of the button click

        # self.button_add.bind(on_press=SalesScreen.to_categories)

        root.add_widget(self.button_add)

        # reports
        self.button_report = Button(text='Reports',
                                    size_hint=(0.15, 0.1),
                                    pos_hint={'right': 1 - 0.01, 'center_y': 0.075})
        # def callback1(instance):
        # in response of the button click
        # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'

        # button_report.bind(on_press=enter_btn_pressed)
        root.add_widget(self.button_report)

        # display the item name and total in this place. This widget could be changed
        self.label1 = Label(text=self.bar_str + self.qty_str,
                            color=(0, 0, 0, 1),
                            pos=(0.9, 0.9),
                            )
        root.add_widget(self.label1)

        with root.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
            # return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def sell_key(self, event):
        self.sell()

    def setupDatabase(self):
        report = setupDatabase()
        if report == {}:

            messagebox("Info", "Database is already setup")
        else:
            messagebox("Info", json.dumps(report))

    def sellAll(self, customername, paymentmode, invoice_no, tip=0):
        try:

            if len(self.basket) == 0:
                raise EmptyBasketError

            for i in self.basket:
                # {"barcode": self.bar_str, "Item Name": record.itemname,"quantity": str(self.quantity_.text), "amount": total_price}
                barcodetext = str(i["barcode"])
                quantity_ = int(i["quantity"])

                sellable = InventoryDB()
                sellable = sellable.getInventoryRecodeByBarcode(barcodetext)[0]
                # sellable.quantity = sellable.quantity - int(quantity_)
                remaining = sellable.quantity - int(quantity_)
                if remaining < 0 and sellable.category != "SERVICE":

                    messagebox(title="Warning", message="Quantity not available ")
                    continue
                elif sellable.category == "SERVICE":
                    sellable.quantity = 0
                else:
                    sellable.quantity = sellable.quantity - int(quantity_)
                saved = sellable.save(update=True)

                sold_price = sellable.price * quantity_
                sold_price = sold_price + tip
                sell = Sales(barcode=barcodetext, time=str(datetime.datetime.now()), quantity=quantity_,
                             itemname=sellable.itemname, amount=sold_price, category=sellable.category,
                             invoice_no=invoice_no, customername=customername, paymentmode=paymentmode)
                sold = sell.save(insert=True)
                if saved == 1 and sold == 1:

                    # messagebox(title="Success",
                    #            message="Item {} of quantity {} sold successfully..\nTotal amount :  {}".format(
                    #                sellable.itemname,
                    #                quantity_))
                    self.barcode_text.text = ""
                    log(activity="Sales", transactiontype="sale", amount=sold_price, barcode=barcodetext,
                        time=str(datetime.datetime.now()))
                    # self.label1.text = ""
                    # self.basket.clear()
                    # print(self.basket)
                    if sellable.quantity <= config.STOCK_LIMIT:
                        try:
                            send_mail(subject="Stock Update",
                                      message="The stock for {} is finished up. Current available stock is {} . Please add some stock to the inventory".format(
                                          sellable.itemname, sellable.quantity))
                        except  smtplib.SMTPServerDisconnected:
                            messagebox(title="Warning", message="Mailing configuration isn't setup")

            messagebox(title="Success",
                       message="Order successful")

            self.label1.text = ""
            self.basket.clear()
            self.quantity_.text = "1"
            print(self.basket)

        except IndexError:
            messagebox(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.text))
            self.barcode_text.text = ""
        except EmptyBasketError:
            messagebox(title="Oops!", message="Nothing to sell")

    # def sellAll(self, customername,paymentmode):

    #     try:
    #         invoice_no = generateInvoiceNumber()
    #         if len(self.basket) == 0:
    #             raise EmptyBasketError
    #         else:
    #             for i in self.basket:
    #                 # {"barcode": self.bar_str, "Item Name": record.itemname,"quantity": str(self.quantity_.text), "amount": total_price}
    #                 barcodetext = str(i["barcode"])
    #                 quantity_ = int(i["quantity"])
    #
    #                 sellable = InventoryDB()
    #                 sellable = sellable.getInventoryRecodeByBarcode(barcodetext)[0]
    #                 # sellable.quantity = sellable.quantity - int(quantity_)
    #                 remaining = sellable.quantity - int(quantity_)
    #                 print(remaining < 0 and sellable.category != "SERVICE")
    #                 if remaining < 0 and sellable.category != "SERVICE":
    #                     messagebox(title="Warning", message="Quantity not available ")
    #                     continue
    #                 elif sellable.category == "SERVICE":
    #                     sellable.quantity = 0
    #                 else:
    #                     sellable.quantity = sellable.quantity - int(quantity_)
    #
    #                 sold_price = sellable.price * quantity_
    #
    #                 total = 0
    #                 for s in self.basket:
    #                     total = total + s["amount"]
    #
    #                 print("After dialog")
    #                 saved = sellable.save(update=True)
    #                 sell = Sales(barcode=barcodetext, time=str(datetime.datetime.now()), quantity=quantity_,
    #                              itemname=sellable.itemname, amount=sold_price, category=sellable.category,
    #                              invoice_no=invoice_no, customername=customername, paymentmode=paymentmode)
    #                 sold = sell.save(insert=True)
    #                 if saved == 1 and sold == 1:
    #
    #                     # messagebox(title="Success",
    #                     #            message="Item {} of quantity {} sold successfully..\nTotal amount :  {}".format(
    #                     #                sellable.itemname,
    #                     #                quantity_))
    #                     self.barcode_text.text = ""
    #                     log(activity="Sales", transactiontype="sale", amount=sold_price, barcode=barcodetext,
    #                         time=str(datetime.datetime.now()))
    #                     # self.label1.text = ""
    #                     # self.basket.clear()
    #                     # print(self.basket)
    #                     if sellable.quantity <= config.STOCK_LIMIT:
    #                         try:
    #                             send_mail(subject="Stock Update",
    #                                       message="The stock for {} is finished up. Current available stock is {} . Please add some stock to the inventory".format(
    #                                           sellable.itemname, sellable.quantity))
    #                         except  smtplib.SMTPServerDisconnected:
    #                             messagebox(title="Warning", message="Mailing configuration isn't setup")
    #
    #                     # messagebox(title="Success",
    #                     #            message="For the Items sold\n Total Amount to be collected : {}".format("gf"))
    #
    #                     self.label1.text = ""
    #                     self.basket.clear()
    #                     self.quantity_.text = "1"
    #                     print(self.basket)
    #
    #             self.sellPopUp(
    #                 "Invoice # {} \n Total Amount ${}".format(invoice_no, total))
    #     except IndexError:
    #         messagebox(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.text))
    #         self.barcode_text.text = ""
    #     except EmptyBasketError:
    #         messagebox(title="Oops!", message="Nothing to sell")

    def sell(self):
        try:
            # print("Sell called")

            barcodetext = str(self.barcode_text.text)
            quantity_ = int(self.quantity_.text)
            # print(quantity_)
            sellable = InventoryDB()
            sellable = sellable.getInventoryRecodeByBarcode(barcodetext)
            # print(sellable)
            sellable = sellable[0]
            if (sellable.quantity >= quantity_):
                sellable.quantity = sellable.quantity - quantity_
                saved = sellable.save(update=True)
                sold_price = sellable.price * quantity_
                sell = Sales(barcode=barcodetext, time=str(datetime.datetime.now()), quantity=quantity_,
                             itemname=sellable.itemname, amount=sold_price, category=sellable.category)
                sold = sell.save(insert=True)
                if saved == 1 and sold == 1:
                    messagebox(title="Success",
                               message="Item {} of quantity {} sold successfully".format(sellable.itemname,
                                                                                         quantity_))
                    self.barcode_text.text = ""
                    log(activity="Sales", transactiontype="sale", amount=sold_price, barcode=barcodetext,
                        time=str(datetime.datetime.now()))
                else:
                    messagebox(title="Failed", message="Could not sell {}".format(self.barcode_text.text))
            elif sellable.quantity == 0:
                send_mail(subject="Stock Update",
                          message="The stock for {} is finished up. Please add some stock to the inventory".format(
                              sellable.itemname))
                messagebox(title="Oops..", message="The stock is empty. A Remainder mail is sent to you")
            else:
                messagebox(title="Sorry :(",
                           message="Stock not available. The available quantity is {} ".format(
                               sellable.quantity))
            if sellable.quantity <= config.STOCK_LIMIT:
                send_mail(subject="Stock Update",
                          message="The stock for {} is finished up. Please add some stock to the inventory".format(
                              sellable.itemname))


        except IndexError:
            messagebox(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.text))
        except TypeError:
            messagebox(title="Failed", message="Barcode not provided")
        except  smtplib.SMTPServerDisconnected:
            messagebox(title="Warning", message="Mailing configuration isn't setup")

    def sellPopUp(self, event):
        if len(self.basket) == 0:
            messagebox(title="Oops", message="Nothing to sell")
            return

        class payment_method:
            method = "cash"
            total = 0

        invoice_no = generateInvoiceNumber()
        total = 0
        for s in self.basket:
            total = total + s["amount"]
        payment_method.total = total
        sellDialog = BoxLayout(orientation="vertical")

        submit = Button(size_hint=(0.2, 0.3), pos_hint={'x': .4, 'y': 0.2}, text="Done")
        cancelbtn = Button(size_hint=(0.2, 0.2), pos_hint={'x': .8}, text="Cancel")

        def tipTextChange(tip):
            print(tip.text)
            try:
                if float(tip.text):
                    payment_method.total = payment_method.total + float(tip.text)
            except:
                tip.text = ""

        tip = TextInput(size_hint=(0.4, 0.3), hint_text="Tip", multiline=False)

        message = "Invoice # {} \n Total Amount ${}".format(invoice_no, payment_method.total)
        msg_label = Label(text=message, size_hint=(None, 0.3), pos_hint={'x': .4})
        customer_name = TextInput(size_hint=(1, None), hint_text="Customer Name", multiline=False)

        sellDialog.add_widget(cancelbtn)
        sellDialog.add_widget(tip)
        sellDialog.add_widget(customer_name)

        tip.bind(on_text=tipTextChange)
        checboxGroup = BoxLayout(orientation="horizontal", size_hint=(None, 0.3), )
        cash_label = Label(text="Cash", size_hint=(None, None))
        card_label = Label(text="Card", size_hint=(None, None))
        cash = CheckBox(size_hint=(None, None), state="down")
        card = CheckBox(size_hint=(None, None))

        def on_checkbox_card(checkbox, value):
            print(value)
            # cash.state = "normal"
            if value:
                payment_method.method = "card"
                cash.state = "normal"

        def on_checkbox_cash(checkbox, value):
            # card.state = "normal"
            if value:
                payment_method.method = "cash"
                card.state = "normal"

        card.bind(active=on_checkbox_card)
        cash.bind(active=on_checkbox_cash)

        checboxGroup.add_widget(cash_label)
        checboxGroup.add_widget(cash)
        checboxGroup.add_widget(card_label)
        checboxGroup.add_widget(card)

        sellDialog.add_widget(msg_label)
        sellDialog.add_widget(checboxGroup)
        sellDialog.add_widget(submit)
        popup = Popup(content=sellDialog, title="Sell Items", auto_dismiss=False, size_hint=(None, None),
                      size=(500, 450))
        popup.open()

        def close_btn(event):
            print(customer_name.text, payment_method.method)
            popup.dismiss()
            tip_=0
            try:
                tip_ = float(tip)
            except Exception:
                messagebox(title="Error",message="Tip must be a Numeric value")
            self.sellAll(customername=customer_name.text, paymentmode=payment_method.method, invoice_no=invoice_no,tip=tip_)
            payment_method.method = "cash"

        def cancel(event):
            popup.dismiss()

        submit.bind(on_press=close_btn)
        cancelbtn.bind(on_press=cancel)

        return (customer_name.text, payment_method.method)


class SalesPage(App):
    def build(self):
        return SalesPageLayout()


if __name__ == '__main__':
    SalesPage().run()
