from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import StringProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

import os
from backend.models import InventoryDB
from backend.utils import messagebox
from views.edititem import Edit
import datetime


class EditableTable(Screen):
    def __init__(self, dataList, title):
        self.name = "editabletable"
        super(EditableTable, self).__init__()
        parent_layout = FloatLayout()
        self.title = str(title)
        scroll_layout = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_layout.bind(size=self._update_rect, pos=self._update_rect)
        table_layout = GridLayout(cols=len(dataList[0]) + 1, size_hint_y=None, spacing=5)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        # table_layout.bind(size=self._update_rect, pos=self._update_rect)
        length = len(dataList[0])

        #
        # for record in dataList:
        #
        #     for p, column in enumerate(record):
        #         if len(str(column)) > sizes[p]:
        #             sizes[p] = len(str(column)) + 3
        self.company = Button(text='Back|',
                              color=(0, 0, 0, 1),
                              background_color=(0, 0, 0, 0),
                              font_size=20,
                              on_press=self.back,
                              pos_hint={'center_x': 0.12, 'center_y': 0.95})
        table_layout.add_widget(self.company)
        # self.company.bind(on_press=lambda m: print("hello"))
        table_layout.add_widget(Label(text="KAKABOKA", size_hint_y=None, color=(0, 0, 0, 1),
                                      font_size=20, ))
        i = 0
        while i < length - 1:
            table_layout.add_widget(Label(text="", size_hint_y=None, height=50))
            i = i + 1
        dataList[0].reverse()
        for i, row_data in enumerate(dataList[0]):
            t = Label(text=row_data, size_hint_y=None, height=40, color=(0, 0, 0, 1))
            table_layout.add_widget(t, index=i)
        table_layout.add_widget(Label(text=""))
        dataList = dataList[1:]

        for row_n, row_data in enumerate(dataList):
            row_data.reverse()
            row_data.append("")
            for i, row in enumerate(row_data):
                new_row = row_data
                t = TextInput(hint_text=str(row), text=str(row), disabled=True, size_hint_y=None, height=40,
                              multiline=False)
                if i <= length - 1:

                    table_layout.add_widget(t, index=i)

                    def changeText(event, data):

                        new_row[i] = data
                        print(data)

                    t.bind(text=changeText)
                else:
                    btn = Button(text="Edit", size_hint_y=None, height=40)
                    btn.barcode_prop = StringProperty()
                    btn.category_prop = StringProperty()
                    btn.barcode_prop = row_data[5]
                    btn.category_prop = row_data[0]
                    btn.bind(on_press=self.updateRecord)
                    table_layout.add_widget(btn)

        with scroll_layout.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=scroll_layout.size, pos=scroll_layout.pos)

        scroll_layout.add_widget(table_layout)
        self.add_widget(scroll_layout)

        self.add_widget(parent_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def updateRecord(self, button):
        barcode = button.barcode_prop
        category = button.category_prop
        print(category)
        # messagebox(title="Info",
        #            message="Editing Barcode : {}\nEditing record will be completed soon!".format(
        #                barcode))
        # print("Record to be updated : {} ".format(barcode))
        edit_page = EditItemScreen(barcode=str(barcode), category=str(category))
        self.manager.add_widget(edit_page)
        self.manager.current = "edititem"
        # db = InventoryDB()
        # data = db.getInventoryRecodeByBarcode(barcode=new_row[5])[0]

        # data.id = new_row[5]
        # data.barcode = new_row[5]
        # data.price = float(3)
        # data.itemname = itemname
        # data.manufacturer = manufacturer
        # data.quantity = quantity
        # data.category = str(new_row[0])
        # print(row_data)

    def back(self, event):
        self.manager.current = "reports"
        self.manager.remove_widget(self)


class EditItemScreen(Screen):
    def __init__(self, **kwargs):
        self.name = "edititem"
        super(EditItemScreen, self).__init__()
        # self.category = self.manager
        l = Edit(barcode=str(kwargs["barcode"]), category=str(kwargs["category"]))
        # l.barcode = StringProperty()
        # l.barcode = kwargs["barcode"]
        # l.company.bind(on_press=self.toHome)
        self.add_widget(l)
        l.company.bind(on_press=self.goBack)

    def goBack(self, button):
        self.manager.current = "editabletable"
        self.manager.remove_widget(self)


class ReadOnlyTable(Screen):
    def __init__(self, dataList, title):
        self.name = "readonlytable"
        super(ReadOnlyTable, self).__init__()
        parent_layout = FloatLayout()
        self.title = str(title)
        scroll_layout = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_layout.bind(size=self._update_rect, pos=self._update_rect)
        table_layout = GridLayout(cols=len(dataList[0]) + 1, size_hint_y=None, spacing=5)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        # table_layout.bind(size=self._update_rect, pos=self._update_rect)
        length = len(dataList[0])

        #
        # for record in dataList:
        #
        #     for p, column in enumerate(record):
        #         if len(str(column)) > sizes[p]:
        #             sizes[p] = len(str(column)) + 3
        self.company = Button(text='Back|',
                              color=(0, 0, 0, 1),
                              background_color=(0, 0, 0, 0),
                              font_size=20,
                              on_press=self.back,
                              pos_hint={'center_x': 0.12, 'center_y': 0.95})
        table_layout.add_widget(self.company)

        table_layout.add_widget(Label(text="KAKABOKA", size_hint_y=None, color=(0, 0, 0, 1),
                                      font_size=20, ))
        table_layout.add_widget(Label(text="Sales", size_hint_y=None, height=50, color=(0, 0, 0, 1), font_size=20))
        table_layout.add_widget(
            Button(text="Show stats", size_hint_y=None, height=50, font_size=10, on_press=self.stats))

        forsales = dataList[1:]
        total_sale = 0
        for d in forsales:
            total_sale = total_sale + float(d[5])
        table_layout.add_widget(Label(text="", size_hint_y=None, height=50))
        table_layout.add_widget(
            Label(text="Total Sales: ${}".format(total_sale), size_hint_y=None, height=50,
                  color=(0, 0, 0, 1), font_size=17))

        i = 0
        while i < length - 5:
            table_layout.add_widget(Label(text="", size_hint_y=None, height=50))
            i = i + 1

        dataList[0].reverse()
        for i, row_data in enumerate(dataList[0]):
            t = Label(text=row_data, size_hint_y=None, height=40, color=(0, 0, 0, 1))
            table_layout.add_widget(t, index=i)

        dataList = dataList[1:]

        table_layout.add_widget(Label(text=""))
        self.dataList = dataList
        for row_n, row_data in enumerate(dataList):
            row_data.reverse()
            row_data.append("")
            for i, row in enumerate(row_data):
                new_row = row_data
                t = Label(text=str(row), size_hint_y=None, font_size=14, pos_hint={"x_center": 0.9}, height=40,
                          color=(0, 0, 0, 1))
                if i <= length - 1:

                    table_layout.add_widget(t, index=i)

                    def changeText(event, data):

                        new_row[i] = data
                        print(data)

                    t.bind(text=changeText)
                else:
                    btn = Label(text="", size_hint_y=None, height=40, color=(0, 0, 0, 1))

                    def updateRecord(self):
                        print("Record to be updated : ")

                        db = InventoryDB()
                        data = db.getInventoryRecodeByBarcode(barcode=new_row[5])[0]
                        data.id = new_row[5]
                        data.barcode = new_row[5]
                        data.price = float(3)
                        # data.itemname = itemname
                        # data.manufacturer = manufacturer
                        # data.quantity = quantity
                        data.category = str(new_row[0])
                        print(row_data)

                    btn.bind(on_press=updateRecord)

                    table_layout.add_widget(btn)

        with scroll_layout.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=scroll_layout.size, pos=scroll_layout.pos)

        scroll_layout.add_widget(table_layout)
        self.add_widget(scroll_layout)

        self.add_widget(parent_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def back(self, event):
        self.manager.current = "reports"
        self.manager.remove_widget(self)

    def stats(self, event):
        sales_data = {"shampoo": 0, "conditioner": 0, "skincare": 0, "haircolor": 0, "misc": 0, "service": 0}
        quantity_data = {"shampoo": 0, "conditioner": 0, "skincare": 0, "haircolor": 0, "misc": 0, "service": 0}
        """
        Categories : 
        CONDITIONER
        SHAMPOO
        SKINCARE
        HAIR COLOR
        MISC
        SERVICE
        """
        # Collecting data to be plotted on the graph
        for d in self.dataList:
            if "shampoo" in d or "SHAMPOO" in d:
                sales_data["shampoo"] = float(sales_data["shampoo"]) + float(d[1])
                quantity_data["shampoo"] = float(quantity_data["shampoo"]) + float(d[2])
            elif "conditioner" in d or "CONDITIONER" in d:
                sales_data["conditioner"] = float(sales_data["conditioner"]) + float(d[1])
                quantity_data["conditioner"] = float(quantity_data["conditioner"]) + float(d[2])
            elif "skincare" in d or "SKINCARE" in d:
                sales_data["skincare"] = float(sales_data["skincare"]) + float(d[1])
                quantity_data["skincare"] = float(quantity_data["skincare"]) + float(d[2])
            elif "HAIR COLOR" in d or "hair color" in d:
                sales_data["haircolor"] = float(sales_data["haircolor"]) + float(d[1])
                quantity_data["haircolor"] = float(quantity_data["haircolor"]) + float(d[2])
            elif "misc" in d or "MISC" in d:
                sales_data["misc"] = float(sales_data["misc"]) + float(d[1])
                quantity_data["misc"] = float(quantity_data["misc"]) + float(d[2])
            elif "service" in d or "SERVICE" in d:
                sales_data["service"] = float(sales_data["service"]) + float(d[1])
                quantity_data["service"] = float(quantity_data["service"]) + float(d[2])

        print(sales_data)
        import matplotlib.pyplot as plt
        import numpy as np
        commodities = ['Shampoo ({})'.format(int(quantity_data["shampoo"])),
                       'Conditioner ({})'.format(int(quantity_data["conditioner"])),
                       'Skin Care ({})'.format(int(quantity_data["skincare"])),
                       'Hair Color ({})'.format(int(quantity_data["haircolor"])),
                       'Misc. ({})'.format(int(quantity_data["misc"])),
                       'Services ({})'.format(int(quantity_data["service"]))]
        sales = [
            sales_data["shampoo"],
            sales_data["conditioner"],
            sales_data["skincare"],
            sales_data["haircolor"],
            sales_data["misc"],
            sales_data["service"],

        ]

        def plot_bar_x():
            # this is for plotting purpose
            index = np.arange(len(commodities))
            print(index)
            plt.bar(index, sales)
            plt.ylabel('Total Sales in USD', fontsize=10)
            plt.xlabel('Commodity', fontsize=10)
            plt.xticks(index, commodities, fontsize=8, rotation=30)
            plt.title('Total Sales of Commodities for date {}'.format(self.dataList[0][3]))
            plt.show()

        plot_bar_x()


class ROTable(Screen):
    def __init__(self, dataList):
        self.name = "editabletable"
        super(ROTable, self).__init__()
        parent_layout = StackLayout()
        scroll_layout = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        table_layout = GridLayout(cols=6, size_hint_y=None, spacing=5)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        length = len(dataList[0])

        sizes = [0] * length

        # for record in dataList:
        #
        #     for p, column in enumerate(record):
        #         if len(str(column)) > sizes[p]:
        #             sizes[p] = len(str(column)) + 3



        for row_n, row_data in enumerate(dataList):
            for i, row in enumerate(row_data.reverse()):
                if i <= len(row_data) - 2:
                    t = Label(hint_text=row, size_hint_y=None, height=40, font_size='20sp')
                    table_layout.add_widget(t, index=i)
                else:
                    btn = Button(text="Update", size_hint_y=None, height=40)
                    table_layout.add_widget(btn, index=i)

        scroll_layout.add_widget(table_layout)
        self.add_widget(parent_layout)
        self.add_widget(scroll_layout)


class DataButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
