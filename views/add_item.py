from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

import pymysql
import datetime
import os
from backend import models
from backend.utils import messagebox


class AddItems(FloatLayout):
    title = 'KAKABOKA'
    manufacturer_filled = ""
    quantity_prefilled = 0

    def __init__(self, **kwargs):
        super(AddItems, self).__init__()
        try:
            self.category = kwargs["category"]
            self.manufacturer_filled = kwargs["manufacturer"]
            self.quantity_prefilled = kwargs["pre_quantity"]
            root = self
            root.bind(size=self._update_rect, pos=self._update_rect)
            self.bar_str = ''
            self.qty_str = ''

            # Product name label
            label_qty = Label(text='Product',
                              color=(0, 0, 0, 0.25),
                              font_size=20,
                              pos_hint={'center_x': 0.175, 'center_y': 0.9})
            root.add_widget(label_qty)

            # barcode label
            label_bar = Label(text='Barcode',
                              color=(0, 0, 0, 0.25),
                              font_size=20,
                              pos_hint={'center_x': 0.175, 'center_y': 0.8})
            root.add_widget(label_bar)

            # quantity label
            self.label_qty = Label(text='Quantity',
                              color=(0, 0, 0, 0.25),
                              font_size=20,
                              pos_hint={'center_x': 0.175, 'center_y': 0.7})
            root.add_widget(self.label_qty)

            # price label
            label_price = Label(text='Price',
                                color=(0, 0, 0, 0.25),
                                font_size=20,
                                pos_hint={'center_x': 0.175, 'center_y': 0.6})
            root.add_widget(label_price)

            # price label
            label_man = Label(text='Manufacturer',
                              color=(0, 0, 0, 0.25),
                              font_size=20,
                              pos_hint={'center_x': 0.175, 'center_y': 0.5})
            root.add_widget(label_man)

            # Category label
            label_category = Label(text="Category",
                                   color=(0, 0, 0, 0.25),
                                   font_size=20,
                                   pos_hint={'center_x': 0.175, 'center_y': 0.4}
                                   )
            root.add_widget(label_category)
            # text box for Product name
            self.itemname = TextInput(hint_text='Name',
                                      multiline=False,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.9},
                                      size_hint=(0.5, 0.075))
            root.add_widget(self.itemname)
            # text box for barcode
            self.barcode = TextInput(hint_text='barcode',
                                     multiline=False,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                     size_hint=(0.5, 0.075),
                                     on_text_validate=self.fetch)

            self.fetch_btn = Button(text="Fetch",
                                    pos_hint={"center_x": 0.84, 'center_y': 0.8},
                                    size_hint=(.15, .07),
                                    on_press=self.fetch
                                    )

            def on_text(instance, value):
                # use try to check if value in database
                self.bar_str = self.barcode.text

            self.barcode.bind(text=on_text)
            root.add_widget(self.barcode)
            root.add_widget(self.fetch_btn)
            # text box for quantity
            self.quantity = TextInput(text=self.quantity_prefilled,
                                      multiline=False,
                                      hint_text="Quantity",
                                      pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                      size_hint=(0.5, 0.075))

            root.add_widget(self.quantity)

            # Available quantity
            self.available = Label(text="",
                                   pos_hint={'center_x': 0.85, 'center_y': 0.7},
                                   size_hint=(0.5, 0.075),
                                   color=(0, 0, 0, 1)
                                   )
            root.add_widget(self.available)

            # text box for Price
            self.price = TextInput(hint_text='USD',
                                   multiline=False,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                   size_hint=(0.5, 0.075))
            root.add_widget(self.price)

            # text box for Manufacturer
            self.man = TextInput(hint_text='Brand',
                                 text=self.manufacturer_filled,
                                 multiline=False,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(0.5, 0.075))
            root.add_widget(self.man)
            self.category_entry = TextInput(hint_text='Product Category',
                                            multiline=False,
                                            disabled=True,
                                            text=self.category,
                                            pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                            size_hint=(0.5, 0.075))
            root.add_widget(self.category_entry)
            # company name
            self.company = Button(text='KAKABOKA',
                                  color=(0, 0, 0, 1),
                                  background_color=(0, 0, 0, 0),
                                  font_size=30,
                                  size_hint=(.25, .07),
                                  pos_hint={'center_x': 0.12, 'center_y': 0.95})
            root.add_widget(self.company)

            # Done button
            donebtn = Button(text='Done',
                             size_hint=(0.2, 0.15),
                             pos_hint={'center_x': 0.5, 'center_y': 0.2})

            def callback2(instance):
                print("Callback 2")

            donebtn.bind(on_press=self.addItem)
            root.add_widget(donebtn)

            with root.canvas.before:
                base_folder = os.path.dirname(__file__)
                image_path = os.path.join(base_folder, 'background.png')
                self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
                # return root
        except:
            messagebox(message="Category Not provided", title="Error!")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def addItem(self, event):
        try:
            itemname = self.itemname.text
            itembarcode = self.barcode.text
            price = float(self.price.text)
            manufacturer = self.man.text
            quantity = int(self.quantity.text)

            if len(itemname) == 0 or len(itembarcode) == 0 or len(self.price.text) == 0 or len(
                    manufacturer) == 0 or len(self.price.text) == 0:
                messagebox(title="Oops!", message="All fields are required. Please fill all fields to continue")
                return

            item = models.Inventory(itemname=itemname, price=price, barcode=str(itembarcode), manufacturer=manufacturer,
                                    quantity=quantity, sold=0, category=self.category)
            saved = item.save(insert=True)
            if saved == 1:
                messagebox(title="Success", message="Item {} added successfully".format(itemname))

                self.itemname.text = ""
                self.barcode.text = ""
                self.price.text = ""
                self.man.text = ""
                self.quantity.text = ""
                self.available.text = ""
                self.label_qty.text = "Quantity"
                models.log(activity="Item Addition", transactiontype="additem", amount=0, barcode=itembarcode,
                           time=str(datetime.datetime.now()))
            else:
                messagebox(title="Failed", message="Could not add {}".format(itemname))
        except ValueError:
            messagebox(title="Warning", message="Price, quantity, barcode must be a Numbers")
        except pymysql.err.IntegrityError:
            # messagebox.showinfo(title="Error",
            #                     message="Item with same barcode cannot be added multiple times. Use update button to update the item details ")
            # p = Popup(title="Are you sure?",
            #           content=Label(
            #               text="Are you sure to overwrite the existing data for {}".format(self.itemname.text)),
            #           size_hint=(None, None), size=(400, 200))
            # p.open()
            # itembarcode = self.barcode.text
            # inventory_db = models.InventoryDB()
            # record = inventory_db.getInventoryRecodeByBarcode(itembarcode)[0]
            # self.quantity_update = str(record.quantity)
            # self.category_entry.text = record.category
            # self.category = record.category
            self.addItem_cascade()

    def addItem_cascade(self):
        try:
            itemname = self.itemname.text
            itembarcode = self.barcode.text
            price = float(self.price.text)
            manufacturer = self.man.text
            quantity = int(self.quantity.text)
            quantity = int(self.quantity_update) + quantity
            item = models.Inventory(itemname=itemname, price=price, barcode=str(itembarcode), manufacturer=manufacturer,
                                    quantity=quantity, sold=0, id=self.id, category=self.category)
            saved = item.save(update=True)
            if saved == 1 or saved == 0:
                # messagebox.showinfo(title="Success", message="Item {} updated successfully".format(itemname))
                popup = Popup(title='Success',
                              content=Label(text="Item {} updated successfully".format(itemname)),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                self.itemname.text = ""
                self.barcode.text = ""
                self.price.text = ""
                self.man.text = ""
                self.quantity.text = ""
                self.available.text = ""
                self.label_qty.text = "Quantity"
                models.log(activity="Item modification", transactiontype="modify", amount=0, barcode=itembarcode,
                           time=str(datetime.datetime.now()))
            else:
                messagebox(title="Failed", message="Nothing to update in  {}".format(itemname))
        except ValueError:
            messagebox(title="Warning", message="Price, quantity, barcode must be a Numbers")
        except AttributeError:
            messagebox(title="Oops!", message="Seems like the item is already present in the database. \n"
                                              "Please fill in the barcode field and press \"Enter\" key to get all the details"
                                              "\nof the item and update corresponding fields")

    def fetch(self, event):

        itembarcode = self.barcode.text
        if len(itembarcode) == 0:
            messagebox(title="Failed", message="Please enter a barcode to fetch details")
            return
        inventory_db = models.InventoryDB()
        record = inventory_db.getInventoryRecodeByBarcode(itembarcode)
        if record == []:
            messagebox(title="Failed", message="Item with this barcode does not exist")
            return
        record = record[0]

        self.id = record.id
        self.price.text = str(record.price)
        self.itemname.text = record.itemname
        self.label_qty.text = "Additional Qty."
        self.available.text = "Available: {}".format(record.quantity)
        self.quantity.text = str(1)
        self.man.text = record.manufacturer
        self.category_entry.text = record.category
        self.category = record.category
        self.quantity_update = str(record.quantity)


class AddItemsApp(App):
    def build(self):
        return AddItems()


if __name__ == '__main__':
    AddItemsApp(category="shampoo").run()
