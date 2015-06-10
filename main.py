import periodictable as pt
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
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from thermo import Thermo
from moles import WaFF
from acidbase import AcidBase


class MainMenu(Widget):

    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        with self.canvas:
            BorderImage(source='bg.png', size=(800, 600))
        self.ab = Button(text='Thermochemistry', pos=(200, 200), on_release=self.use_thermo,
                         background_color=(.5, .2, .5, 1))
        self.ac = Button(text='Moles/Atoms', pos=(325, 200), on_release=self.use_moles,
                         background_color=(.5, .2, .5, 1))
        self.ad = Button(text='AcidBase', pos=(450, 200), on_release=self.use_ab,
                         background_color=(.5, .2, .5, 1))
        self.credit = Label(text='Made by Columbus Holt', pos=((800 - 150), (600 - self.height)))
        self.add_widget(self.credit)
        self.add_widget(self.ab)
        self.add_widget(self.ac)
        self.add_widget(self.ad)

    def use_thermo(self, *args):
        self.clean()
        self.add_widget(Thermo())

    def use_moles(self, *args):
        self.clean()
        self.add_widget(WaFF())

    def use_ab(self, *args):
        self.clean()
        self.add_widget(AcidBase())

    def clean(self, *args):
        self.clear_widgets()
        self.add_widget(Button(text='Return to Main', x=700, on_release=self.re_add,
                               background_color=(.5, .2, .5, 1)))

    def re_add(self, *args):
        self.clear_widgets()
        self.add_widget(self.credit)
        self.add_widget(self.ab)
        self.add_widget(self.ac)
        self.add_widget(self.ad)


class Main(App):

    def build(self):
        return MainMenu()

if __name__ == '__main__':
    Main().run()