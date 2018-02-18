import os

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from backend.utils import messagebox
import json
from backend.models import InventoryDB, Sales, log
from backend.utils import send_mail
from backend.database import *
import datetime
import os
import json
from views import categories_kivy


class SalesPage(App):
    title = 'KAKABOKA'
    basket = []

    def build(self):
        self.root = root = FloatLayout()
        root.bind(size=self._update_rect, pos=self._update_rect)
        self.bar_str = ''
        self.qty_str = ''

        # barcode label
        label_qty = Label(text='Quantity',
                          color=(0, 0, 0, 0.25),
                          font_size=20,
                          pos_hint={'center_x': 0.175, 'center_y': 0.7})
        root.add_widget(label_qty)

        # quantity label
        label_bar = Label(text='Barcode',
                          color=(0, 0, 0, 0.25),
                          font_size=20,
                          pos_hint={'center_x': 0.175, 'center_y': 0.8})
        root.add_widget(label_bar)
        # text box for barcode
        self.barcode_text = TextInput(hint_text='barcode',
                                      multiline=False,
                                      on_text_validate=self.sell_key,
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

                if len(self.barcode_text.text) == 0:
                    messagebox(title='Warning', message="Please enter the barcode")
                    return
                else:
                    obj = {"barcode": self.bar_str, "quantity": str(self.quantity_.text)}
                    self.basket.append(obj)
                    # label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'
                    label1.text = label1.text + json.dumps(obj) + "\n"
            except TypeError:
                messagebox(title="Failed", message="Quantity must be a Numeric value")

        enter_btn.bind(on_press=enter_btn_pressed)
        root.add_widget(enter_btn)

        # To finish entry and get the final total.
        done_btn = Button(text='Done',
                          size_hint=(0.2, 0.15),
                          pos_hint={'center_x': 0.5, 'center_y': 0.2})

        # def callback2(instance):
        #     label1.text = label1.text + '\n Done'

        done_btn.bind(on_press=self.sell_key)
        root.add_widget(done_btn)

        # add item
        button_add = Button(text='+',
                            size_hint=(0.15, 0.1),
                            pos_hint={'right': 0.85 - 0.01, 'center_y': 0.075})
        # def callback1(instance):
        # in response of the button click

        button_add.bind(on_press=self.to_categories)

        root.add_widget(button_add)

        # reports
        button_report = Button(text='Reports',
                               size_hint=(0.15, 0.1),
                               pos_hint={'right': 1 - 0.01, 'center_y': 0.075})
        # def callback1(instance):
        # in response of the button click
        # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'

        button_report.bind(on_press=enter_btn_pressed)
        root.add_widget(button_report)

        # display the item name and total in this place. This widget could be changed
        label1 = Label(text=self.bar_str + self.qty_str,
                       color=(0, 0, 0, 1),
                       pos=(0.9, 0.9),
                       )
        root.add_widget(label1)

        with root.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
            return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def to_categories(self, event):
        categories_kivy.Categories().build()

    def sell_key(self, event):
        self.sell()

    def setupDatabase(self):
        report = setupDatabase()
        if report == {}:

            messagebox("Info", "Database is already setup")
        else:
            messagebox("Info", json.dumps(report))

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
            if (sellable.quantity > quantity_):
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
                           message="Stock not available. The available qunatity is {} ".format(
                               sellable.quantity))
        except IndexError:
            messagebox(title="Failed", message="Barcode {} does not exists".format(self.barcode_text.text))
        except TypeError:
            messagebox(title="Failed", message="Barcode not provided")


if __name__ == '__main__':
    SalesPage().run()