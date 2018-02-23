from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class EditableTable(Screen):
    def __init__(self, dataList):
        parent_layout = StackLayout()
        table_layout = GridLayout()

        try:

            length = len(dataList[0])

            sizes = [0] * length

            for record in dataList:

                for p, column in enumerate(record):
                    if len(str(column)) > sizes[p]:
                        sizes[p] = len(str(column)) + 3

            for row_n, row_data in enumerate(dataList):
                for i, row in enumerate(row_data):
                    TextInput(table, text=str(row), width=sizes[i], borderwidth=2, relief="groove", justify=LEFT, anchor=W,
                         background="white").grid(column=i, row=row_n + 1, sticky=W)

        self.add_widget(parent_layout)
        self.add_widget(table_layout)
