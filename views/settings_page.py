import os

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import json
from backend import config
from backend.utils import messagebox


class SettingsPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = self
        root.bind(size=self._update_rect, pos=self._update_rect)

        label_email = Label(text='Email',
                            color=(0, 0, 0, 0.8),
                            font_size=16,
                            pos_hint={'center_x': 0.175, 'center_y': 0.95})
        root.add_widget(label_email)

        textinput_email = TextInput(hint_text='Email',
                                    multiline=False,
                                    pos_hint={'center_x': 0.43, 'center_y': 0.95},
                                    size_hint=(0.35, 0.055))
        root.add_widget(textinput_email)

        root.add_widget(
            Label(text='Password',
                  color=(0, 0, 0, 0.8),
                  font_size=16,
                  pos_hint={'center_x': 0.175, 'center_y': 0.87})
        )
        textinput_password = TextInput(hint_text='Password',
                                       multiline=False,
                                       password=True,
                                       pos_hint={'center_x': 0.43, 'center_y': 0.87},
                                       size_hint=(0.35, 0.055))
        root.add_widget(textinput_password)

        root.add_widget(Label(text='Mail Server',
                              color=(0, 0, 0, 0.8),
                              font_size=16,
                              pos_hint={'center_x': 0.175, 'center_y': 0.79})
                        )

        textinput_mailserver = TextInput(hint_text='mail.example.com',
                                         multiline=False,
                                         pos_hint={'center_x': 0.43, 'center_y': 0.79},
                                         size_hint=(0.35, 0.055))
        root.add_widget(textinput_mailserver)

        root.add_widget(
            Label(text='Port',
                  color=(0, 0, 0, 0.8),
                  font_size=16,
                  pos_hint={'center_x': 0.175, 'center_y': 0.71})
        )
        textinput_port = TextInput(hint_text='Port',
                                   multiline=False,
                                   pos_hint={'center_x': 0.43, 'center_y': 0.71},
                                   size_hint=(0.35, 0.055))
        root.add_widget(textinput_port)

        donebtn = Button(text='Submit',
                         size_hint=(0.2, 0.15),
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})

        def submit(instance):
            if len(textinput_mailserver.text) == 0 or len(textinput_password.text) == 0 or len(
                    textinput_email.text) == 0 or len(textinput_port.text) == 0:
                messagebox(title="Error", message="Please fill in all the details")
            mailsever = textinput_mailserver.text
            password = textinput_password.text
            email = textinput_email.text
            port = textinput_port.text

            config_vals = config.config
            print(mailsever, password, email, port)
            with open(config.config_file,mode='w') as f:
                config_vals["email"] = email
                config_vals["mail_host"] = mailsever
                config_vals["mail_password"] = password
                config_vals["mail_port"] = port
                stringify = json.dumps(config_vals)
                f.write(stringify)
                messagebox(title="Success",message="Configuration written successfully")

        donebtn.bind(on_press=submit)
        root.add_widget(donebtn)

        with root.canvas.before:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'background.png')
            self.rect = Rectangle(source=image_path, size=root.size, pos=root.pos)
            # return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
