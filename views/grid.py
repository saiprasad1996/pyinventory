from kivy.graphics.vertex_instructions import Rectangle
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
                t = TextInput(hint_text=str(row), text=str(row), size_hint_y=None, height=40, multiline=False)
                if i <= length - 1:

                    table_layout.add_widget(t, index=i)

                    def changeText(event, data):

                        new_row[i] = data
                        print(data)

                    t.bind(text=changeText)
                else:
                    btn = Button(text="Update", size_hint_y=None, height=40)

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
        self.company.bind(on_press=lambda m: print("hello"))
        table_layout.add_widget(Label(text="KAKABOKA", size_hint_y=None, color=(0, 0, 0, 1),
                                      font_size=20, ))
        table_layout.add_widget(Label(text="Sales", size_hint_y=None, height=50, color=(0, 0, 0, 1), font_size=20))
        table_layout.add_widget(
            Button(text="Show stats", size_hint_y=None, height=50, font_size=10, on_press=self.stats))
        i = 0
        while i < length - 3:
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
                t = Label(text=str(row), size_hint_y=None, height=40, color=(0, 0, 0, 1))
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

        import matplotlib.pyplot as plt
        import numpy as np
        label = ['Shampoo', 'Conditioner', 'Skin Care', 'Color', 'Misc.', 'Services']
        sales = [
            300, 800, 350, 1000, 500, 650
        ]

        def plot_bar_x():
            # this is for plotting purpose
            index = np.arange(len(label))
            plt.bar(index, sales)
            plt.ylabel('Total Sales upto date {}'.format(str(datetime.datetime.now())[:11]), fontsize=10)
            plt.xlabel('Commodity', fontsize=10)
            plt.xticks(index, label, fontsize=8, rotation=30)
            plt.title('Total Sales of Commodities upto date {}'.format(str(datetime.datetime.now())[:11]))
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
                    t = Label(hint_text=row, size_hint_y=None, height=40)
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
