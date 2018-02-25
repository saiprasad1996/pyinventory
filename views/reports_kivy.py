import datetime

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from backend.utils import messagebox
from backend.models import *

import os
from views import reportstable


class ReportsLayout(FloatLayout):
    def __init__(self):
        super(ReportsLayout, self).__init__()
        root = self
        grid = GridLayout(cols=3,
                          size_hint=(0.5, 0.5),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root.bind(size=self._update_rect, pos=self._update_rect)
        self.bar_str = ''
        self.qty_str = ''

        # company name
        self.company = Button(text='KAKABOKA',
                              color=(0, 0, 0, 1),
                              background_color=(0, 0, 0, 0),
                              font_size=30,
                              pos_hint={'center_x': 0.12, 'center_y': 0.95})
        root.add_widget(self.company)

        # self.stock_report = Button(text='Stock',
        #                       size_hint=(0.2, 0.15),
        #                       on_press=self.renderTableStock)
        self.stock_report = Button(text='Stock',
                                   size_hint=(0.2, 0.15))

        # background_color=(0.5, 0.5, 0.5, 0.75))

        # pos_hint={'right':0.95,'center_y':0.8})
        def callback1(instance):
            # in response of the button click
            label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'

        #
        # stock_report.bind(on_press=callback1)
        grid.add_widget(self.stock_report)

        # conditioners button

        # self.sales_report = Button(text='Sales',
        #                            on_press=self.renderTableSales,
        #                            size_hint=(0.2, 0.15))
        self.sales_report = Button(text='Sales',

                                   size_hint=(0.2, 0.15))


        # pos_hint={'right':0.85-0.01,'center_y':0.075})
        # def callback1(instance):
        # in response of the button click

        self.sales_report.bind(on_press=callback1)
        grid.add_widget(self.sales_report)

        # services button
        self.button_services = Button(text='Services',
                                      size_hint=(0.2, 0.15))
        # pos_hint={'right':0.85-0.01,'center_y':0.075})
        # def callback1(instance):
        # in response of the button click


        grid.add_widget(self.button_services)

        self.date_entry = TextInput(
            hint_text="dd/mm/yyyy",
            size_hint=(0.2, None),
            height=30,
            multiline=False)

        # pos_hint={'center_x':0.5,'center_y':0.2})
        date = datetime.datetime.now()
        date = date.strftime("%d/%m/%Y")
        self.date_entry.text = date
        print("Date : " + date)

        def callback2(instance):
            try:
                dateobject = datetime.datetime.strptime(self.date_entry.text, "%d/%m/%Y")
            except Exception:
                messagebox(title="Invalid date format",
                           message="You've entered an invalid date format.\n Please enter a date with the format dd/mm/yyyy")

        self.date_entry.bind(on_text_validate=callback2)
        grid.add_widget(self.date_entry)

        # display the item name and total in this place. This widget could be changed
        label1 = Label(text=self.bar_str + self.qty_str,
                       color=(0, 0, 0, 1),
                       pos=(0.9, 0.9))
        root.add_widget(label1)

        root.add_widget(grid)

        with root.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def renderTableSales(self, event):
        try:
            self.selected_date = self.date_entry.text
            print(self.selected_date)
            selected_date_o = datetime.datetime.strptime(self.selected_date, "%d/%m/%Y")

            datalist = InventoryDB()

            datalist = datalist.getAllSales()
            items = [["ID", "Barcode", "Item Name", "Date", "Quantity", "Selling Amount"]]
            for i in datalist:
                date = datetime.datetime.strptime(str(i.time[:10]), "%Y-%m-%d")
                if selected_date_o == date:
                    items.append([i.id, i.barcode, i.itemname, i.time[:11], i.quantity, i.amount])
            reportstable.renderMatPlot(items)
        except ValueError:
            messagebox(title="Error", message="Please enter a valid date. \nPlease enter the date in dd/mm/yyyy format")

    def renderTableStock(self, event):
        try:
            selected_date = self.date_entry.text
            selected_date_o = datetime.datetime.strptime(selected_date, "%d/%m/%Y")
            datalist = InventoryDB()

            datalist = datalist.getInventory()
            items = [["Sl No", "Barcode", "Item Name", "Price", "Manufacturer", "Quantity", "Category"]]
            for i in enumerate(datalist):
                items.append([i[0] + 1, i[1].barcode, i[1].itemname, i[1].price, i[1].manufacturer, i[1].quantity,
                              i[1].category])

            # reportstable.renderTable(items)
            reportstable.renderMatPlot(items)
        except ValueError:
            messagebox(title="Error", message="Please enter a valid date. \nPlease enter the date in dd/mm/yyyy format")


class Reports(App):
    def build(self):
        return ReportsLayout()



        # class Reports(App):
        #     title = 'KAKABOKA'
        #
        #     def build(self):
        #         self.root = root = FloatLayout()
        #         grid = GridLayout(cols=3,
        #                           size_hint=(0.5, 0.5),
        #                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        #         root.bind(size=self._update_rect, pos=self._update_rect)
        #         self.bar_str = ''
        #         self.qty_str = ''
        #
        #         # company name
        #         label2 = Label(text='KAKABOKA',
        #                        color=(0, 0, 0, 1),
        #                        font_size=30,
        #                        pos_hint={'center_x': 0.12, 'center_y': 0.95})
        #         root.add_widget(label2)
        #
        #         # shampoo button
        #         stock_report = Button(text='Stock',
        #                               size_hint=(0.2, 0.15),
        #                               on_press=self.renderTableStock,
        #                               background_color=(0.5, 0.5, 0.5, 0.75))
        #
        #         # pos_hint={'right':0.95,'center_y':0.8})
        #         def callback1(instance):
        #             # in response of the button click
        #             label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'
        #
        #         #
        #         # stock_report.bind(on_press=callback1)
        #         grid.add_widget(stock_report)
        #
        #         # conditioners button
        #         sales_report = Button(text='Sales',
        #                               on_press=self.renderTableSales,
        #                               size_hint=(0.2, 0.15))
        #         # pos_hint={'right':0.85-0.01,'center_y':0.075})
        #         # def callback1(instance):
        #         # in response of the button click
        #
        #         sales_report.bind(on_press=callback1)
        #         grid.add_widget(sales_report)
        #
        #         # services button
        #         button_services = Button(text='Services',
        #                                  size_hint=(0.2, 0.15))
        #         # pos_hint={'right':0.85-0.01,'center_y':0.075})
        #         # def callback1(instance):
        #         # in response of the button click
        #
        #         button_services.bind(on_press=callback1)
        #         grid.add_widget(button_services)
        #
        #         self.date_entry = TextInput(
        #             hint_text="dd/mm/yyyy",
        #             size_hint=(0.2, None),
        #             height=30,
        #             multiline=False)
        #
        #         # pos_hint={'center_x':0.5,'center_y':0.2})
        #         date = datetime.datetime.now()
        #         date = date.strftime("%d/%m/%Y")
        #         self.date_entry.text = date
        #         print("Date : " + date)
        #
        #         def callback2(instance):
        #             try:
        #                 dateobject = datetime.datetime.strptime(self.date_entry.text, "%d/%m/%Y")
        #             except Exception:
        #                 messagebox(title="Invalid date format",
        #                            message="You've entered an invalid date format.\n Please enter a date with the format dd/mm/yyyy")
        #
        #         self.date_entry.bind(on_text_validate=callback2)
        #         grid.add_widget(self.date_entry)
        #
        #         # display the item name and total in this place. This widget could be changed
        #         label1 = Label(text=self.bar_str + self.qty_str,
        #                        color=(0, 0, 0, 1),
        #                        pos=(0.9, 0.9))
        #         root.add_widget(label1)
        #
        #         root.add_widget(grid)
        #
        #         with root.canvas.before:
        #             base_folder = os.path.dirname(__file__)
        #             image_path = os.path.join(base_folder, 'background.png')
        #             self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
        #             return root
        #
        #     def _update_rect(self, instance, value):
        #         self.rect.pos = instance.pos
        #         self.rect.size = instance.size
        #
        # def renderTableSales(self,event):
        #     try:
        #         selected_date = self.date_entry.text
        #         print(selected_date)
        #         selected_date_o = datetime.datetime.strptime(selected_date, "%d/%m/%Y")
        #
        #         datalist = InventoryDB()
        #
        #         datalist = datalist.getAllSales()
        #         items = [["ID", "Barcode", "Item Name", "Date", "Quantity", "Selling Amount"]]
        #         for i in datalist:
        #             date = datetime.datetime.strptime(str(i.time[:10]), "%Y-%m-%d")
        #             if selected_date_o == date:
        #                 items.append([i.id, i.barcode, i.itemname, i.time[:11], i.quantity, i.amount])
        #         reportstable.renderMatPlot(items)
        #     except ValueError:
        #         messagebox(title="Error",message="Please enter a valid date. \nPlease enter the date in dd/mm/yyyy format")
        # def renderTableStock(self,event):
        #     try:
        #         selected_date = self.date_entry.text
        #         selected_date_o = datetime.datetime.strptime(selected_date, "%d/%m/%Y")
        #         datalist = InventoryDB()
        #
        #         datalist = datalist.getInventory()
        #         items = [["Sl No", "Barcode", "Item Name", "Price", "Manufacturer", "Quantity", "Category"]]
        #         for i in enumerate(datalist):
        #             items.append([i[0] + 1, i[1].barcode, i[1].itemname, i[1].price, i[1].manufacturer, i[1].quantity,
        #                           i[1].category])
        #
        #         # reportstable.renderTable(items)
        #         reportstable.renderMatPlot(items)
        #     except ValueError:
        #         messagebox(title="Error",message="Please enter a valid date. \nPlease enter the date in dd/mm/yyyy format")


if __name__ == '__main__':
    Reports().run()
