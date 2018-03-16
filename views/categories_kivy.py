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
import os


class CategoriesLayout(FloatLayout):
    title = 'KAKABOKA'

    def __init__(self):
        super(CategoriesLayout, self).__init__()
        root = self
        grid = GridLayout(cols=3,
                          size_hint=(0.5, 0.5),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root.bind(size=self._update_rect, pos=self._update_rect)
        self.bar_str = ''
        self.qty_str = ''

        # title label
        label_qty = Label(text='Categories',
                          color=(0, 0, 0, 0.25),
                          font_size=20,
                          pos_hint={'center_x': 0.1, 'top': 0.9})
        root.add_widget(label_qty)

        # company name
        self.company = Button(text='<- KAKABOKA',
                              color=(0, 0, 0, 1),
                              background_color=(0, 0, 0, 0),
                              font_size=30,
                              pos_hint={'center_x': 0.15, 'center_y': 0.95})
        root.add_widget(self.company)

        # shampoo button
        self.button_shampoo = Button(text='Shampoo',
                                     size_hint=(0.2, 0.15),
                                     )

        # pos_hint={'right':0.95,'center_y':0.8})
        def callback1(instance):
            # in response of the button click
            label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'

        # button_shampoo.bind(on_press=callback1)
        grid.add_widget(self.button_shampoo)

        # conditioners button
        self.button_cond = Button(text='Conditioner',
                                  size_hint=(0.2, 0.15))
        # pos_hint={'right':0.85-0.01,'center_y':0.075})
        # def callback1(instance):
        # in response of the button click

        # self.button_cond.bind(on_press=callback1)
        grid.add_widget(self.button_cond)

        # skin care button
        self.button_skin = Button(text='Skin Care',
                                  size_hint=(0.2, 0.15))

        # pos_hint={'center_x':0.5,'center_y':0.2})

        def callback2(instance):
            label1.text = label1.text + '\n Done'

        # self.button_skin.bind(on_press=callback2)
        grid.add_widget(self.button_skin)

        # services button
        self.button_services = Button(text='Services',
                                      size_hint=(0.2, 0.15))
        # pos_hint={'right':0.85-0.01,'center_y':0.075})
        # def callback1(instance):
        # in response of the button click

        self.button_services.bind(on_press=callback1)
        grid.add_widget(self.button_services)

        # Color button
        self.button_color = Button(text='Color',
                                   size_hint=(0.2, 0.15))
        # pos_hint={'right':1-0.01,'center_y':0.075})
        # def callback1(instance):
        # in response of the button click
        # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'

        self.button_color.bind(on_press=callback1)
        grid.add_widget(self.button_color)

        # Misc button
        self.button_Misc = Button(text='Misc',
                                  size_hint=(0.2, 0.15))
        # def callback1(instance):
        # in response of the button click
        # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'

        self.button_Misc.bind(on_press=callback1)
        grid.add_widget(self.button_Misc)

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
            # return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    CategoriesLayout().run()

# class Categories(App):
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
#         # title label
#         label_qty = Label(text='Categories',
#                           color=(0, 0, 0, 0.25),
#                           font_size=20,
#                           pos_hint={'center_x': 0.1, 'top': 0.9})
#         root.add_widget(label_qty)
#
#         # company name
#         label2 = Label(text='KAKABOKA',
#                        color=(0, 0, 0, 1),
#                        font_size=30,
#                        pos_hint={'center_x': 0.12, 'center_y': 0.95})
#         root.add_widget(label2)
#
#         # shampoo button
#         button_shampoo = Button(text='Shampoo',
#                                 size_hint=(0.2, 0.15),
#                                 background_color=(0.5, 0.5, 0.5, 0.75))
#
#         # pos_hint={'right':0.95,'center_y':0.8})
#         def callback1(instance):
#             # in response of the button click
#             label1.text = label1.text + self.bar_str + self.qty_str + '\nEntered\n'
#
#         button_shampoo.bind(on_press=callback1)
#         grid.add_widget(button_shampoo)
#
#         # conditioners button
#         button_cond = Button(text='Services',
#                              size_hint=(0.2, 0.15))
#         # pos_hint={'right':0.85-0.01,'center_y':0.075})
#         # def callback1(instance):
#         # in response of the button click
#
#         button_cond.bind(on_press=callback1)
#         grid.add_widget(button_cond)
#
#         # skin care button
#         button_skin = Button(text='Skin Care',
#                              size_hint=(0.2, 0.15))
#
#         # pos_hint={'center_x':0.5,'center_y':0.2})
#
#         def callback2(instance):
#             label1.text = label1.text + '\n Done'
#
#         button_skin.bind(on_press=callback2)
#         grid.add_widget(button_skin)
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
#         # Color button
#         button_color = Button(text='Color',
#                               size_hint=(0.2, 0.15))
#         # pos_hint={'right':1-0.01,'center_y':0.075})
#         # def callback1(instance):
#         # in response of the button click
#         # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'
#
#         button_color.bind(on_press=callback1)
#         grid.add_widget(button_color)
#
#         # Misc button
#         button_Misc = Button(text='Misc',
#                              size_hint=(0.2, 0.15))
#         # def callback1(instance):
#         # in response of the button click
#         # label1.text=label1.text+self.bar_str + self.qty_str+'\nEntered\n'
#
#         button_Misc.bind(on_press=callback1)
#         grid.add_widget(button_Misc)
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
