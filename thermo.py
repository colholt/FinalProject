
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import BorderImage
from functools import partial
from kivy.animation import Animation
import thermocalc
from thermocalc import thermo

Builder.load_string("""
<WaFF>:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

""")


class Thermo(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(BoxLayout, self).__init__(*args, **kwargs)
        self.mass = TextInput(text='Enter given/mass', multiline=False, size=(300, 50))
        self.mass.bind(on_text_validate=self.set_mass)
        self.mass.bind(focus=self.on_focus)
        self.given = 0
        self.temp1 = 0
        self.temp2 = 0
        self.constant = 0
        self.add_widget(self.mass)
        self.given_label = Label(pos=(525, 200))
        self.temp1_label = Label(pos=(525, 225))
        self.temp2_label = Label(pos=(525, 250))
        self.constant_label = Label(pos=(525, 275))
        self.calculated = Label(pos=(525, 300))
        self.errorlabel = Label(pos=((self.mass.x + 50), (self.mass.y + 100)))
        self.confirm = Button(text='Calculate', x=400)
        self.confirm.bind(on_release=self.calculate)
        self.labels = [self.given_label, self.temp1_label, self.temp2_label,
                       self.constant_label, self.calculated]
        for i in self.labels:
            self.add_widget(i)
        for i in self.labels:
            i.bind(on_focus=partial(self.on_focus, i))

    def set_mass(self, *args):
        try:
            int(self.mass.text)
            self.given = self.mass.text
            self.given_label.text = 'Given: ' + self.given
            self.unbi(self.set_mass)
            self.mass.bind(on_text_validate=self.set_temp1)
            self.set_text('Enter lowest temp')
            try:
                self.remove_widget(self.errorlabel)
            except:
                pass
        except ValueError:
            self.errorlabel.text = 'Invalid input, re-enter given'
            try:
                self.add_widget(self.errorlabel)
            except:
                pass

    def set_temp1(self, *args):
        try:
            int(self.mass.text)
            self.temp1 = self.mass.text
            self.temp1_label.text = 'Low temp: ' + self.temp1
            self.unbi(self.set_temp1)
            self.mass.bind(on_text_validate=self.set_temp2)
            self.set_text('Enter highest temp')
            try:
                self.remove_widget(self.errorlabel)
            except:
                pass
        except ValueError:
            self.errorlabel.text = 'Invalid input, re-enter lowest temp'
            try:
                self.add_widget(self.errorlabel)
            except:
                pass

    def set_temp2(self, *args):
        try:
            int(self.mass.text)
            self.temp2 = self.mass.text
            self.temp2_label.text = 'High temp: ' + self.temp2
            self.unbi(self.set_temp2)
            self.mass.bind(on_text_validate=self.set_constant)
            self.set_text('grams or kJ')
            try:
                self.remove_widget(self.errorlabel)
            except:
                pass
        except ValueError:
            self.errorlabel.text = 'Invalid input, re-enter highest temp'
            try:
                self.add_widget(self.errorlabel)
            except:
                pass

    def set_constant(self, *args):
        self.add_widget(self.confirm)
        if self.mass.text.lower() == 'grams':
            self.constant = 1
            self.constant_label.text = 'constants: grams'
        else:
            self.constant = 0
            self.constant_label.text = 'constants: kilojoules'

    def unbi(self, prop, *args):
        self.mass.unbind(on_text_validate=prop)

    def set_text(self, text, *args):
        self.mass.text = text

    def calculate(self, *args):
        self.calculated.text = str(thermo(float(self.given), int(self.temp1), int(self.temp2), int(self.constant)))

    def on_focus(self, instance, value, *args):
        if value:
            self.mass.text = ''
