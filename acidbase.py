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
import math

constant = 10**-14


def ph(x):
    print('pH = ' + str(float(x)))
    print('H+ = ' + phtoh(x))
    print('OH- = ' + htoh(phtoh(x)))
    get_ab(x, 1)


def h(x):
    print('H+ = ' + str('%.2E' % float(x)))
    print('OH- = ' + htoh(x))
    print('pH = ' + ohtoph(x))


def oh(x):
    print('OH- = ' + str('%.2E' % float(x)))
    h = float(constant) / float(x)
    print('H+ = ' + str('%.2E' % float(h)))
    ph2 = -1 * math.log10(h)
    print('pH = ' + str(float(ph2)))
    get_ab(ph2, 1)


def poh(x):
    print('pOH = ' + str(float(x)))
    oh = 10**(-x)
    print('OH- = ' + str('%.2E' % float(oh)))
    h = float(constant) / float(oh)
    print('H+ = ' + str('%.2E' % float(h)))
    print('pH = ' + str(14 - x))


def htoh(x):
    return str('%.2E' % (float(constant) / float(x)))


def phtoh(x):
    return str('%.2E' % (10**(-x)))


def ohtoph(x):
    print 'pOH = ' + str(14 - (float(-1 * math.log10(x))))
    return str(float(-1 * math.log10(x)))


def get_ab(x, y):
    if y == 1:
        poh = 14 - x
        return 'pOH = ' + str(poh)


def calculation(chemtype):
    if chemtype == 1:
        value = input('what is your pH value?')
        ph(float(value))
    if chemtype == 2:
        value = input('what is your H+ value?')
        h(float(value))
    if chemtype == 3:
        value = input('what is your OH- value?')
        oh(float(value))
    if chemtype == 4:
        value = input('what is your pOH value?')
        poh(float(value))


class AcidBase(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(BoxLayout, self).__init__(*args, **kwargs)
        self.chemt = TextInput(text='1. pH, 2. H+, 3. OH-, 4. pOH', multiline=False,
                               size=(300, 50), input_filter=float)
        self.chemt.bind(focus=self.on_focus)
        self.chemt.bind(on_text_validate=self.setab)
        self.acidbase = 0
        self.errorlab = Label(pos=(self.chemt.x + 50, (self.chemt.y + 100)))
        self.ph = Label(pos=(350, 375))
        self.h = Label(pos=(350, 400))
        self.oh = Label(pos=(350, 425))
        self.poh = Label(pos=(350, 450))
        self.labels = [self.ph, self.h, self.oh, self.poh]
        for i in self.labels:
            self.add_widget(i)
        self.add_widget(self.chemt)

    def setab(self, *args):
        self.acidbase = self.chemt.text
        if self.acidbase == '1':
            self.chemt.text = 'Enter pH value'
            self.chemt.unbind(on_text_validate=self.setab)
            self.chemt.bind(on_text_validate=partial(self.calc, 1))
        elif self.acidbase == '2':
            self.chemt.text = 'Enter H+ value'
            self.chemt.unbind(on_text_validate=self.setab)
            self.chemt.bind(on_text_validate=partial(self.calc, 2))
        elif self.acidbase == '3':
            self.chemt.text = 'Enter OH- value'
            self.chemt.unbind(on_text_validate=self.setab)
            self.chemt.bind(on_text_validate=partial(self.calc, 3))
        elif self.acidbase == '4':
            self.chemt.text = 'Enter pOH value'
            self.chemt.unbind(on_text_validate=self.setab)
            self.chemt.bind(on_text_validate=partial(self.calc, 4))

    def calc(self, x, *args):
        if x == 1:
            try:
                theph = float(self.chemt.text)
                self.ph.text = 'pH = ' + str(theph)
                self.h.text = 'H+ = ' + phtoh(theph)
                self.oh.text = 'OH- = ' + htoh(phtoh(theph))
                self.poh.text = 'pOH = ' + str((14 - theph))
                try:
                    self.remove_widget(self.errorlab)
                except:
                    pass
            except ValueError:
                self.errorlab.text = 'Invalid, enter pH again'
                try:
                    self.add_widget(self.errorlab)
                except:
                    pass
        if x == 2:
                self.ph.text = 'pH = ' + ohtoph(float(self.chemt.text))
                self.h.text = 'H+ = ' + str('%.2E' % float(self.chemt.text))
                self.oh.text = 'OH- = ' + htoh(float(self.chemt.text))
                self.poh.text = 'pOH = ' + str(14 - float(ohtoph(float(self.chemt.text))))
                try:
                    self.remove_widget(self.errorlab)
                except:
                    pass
        if x == 3:
            try:
                he = float(constant) / float(self.chemt.text)
                ph2 = -1 * math.log10(he)
                self.ph.text = 'pH = ' + str(float(ph2))
                self.h.text = 'H+ = ' + str('%.2E' % float(he))
                self.oh.text = 'OH- = ' + str('%.2E' % float(self.chemt.text))
                self.poh.text = 'pOH = ' + str(14 - float(ph2))
                try:
                    self.remove_widget(self.errorlab)
                except:
                    pass
            except ValueError:
                self.errorlab.text = 'Invalid, enter OH- again'
                try:
                    self.add_widget(self.errorlab)
                except:
                    pass
        if x == 4:
            try:
                ohh = 10**(-float(self.chemt.text))
                he = float(constant) / float(ohh)
                self.ph.text = 'pH = ' + str(14 - float(self.chemt.text))
                self.h.text = 'H+ = ' + str('%.2E' % float(he))
                self.oh.text = 'OH- = ' + str('%.2E' % float(ohh))
                self.poh.text = 'pOH = ' + self.chemt.text
                try:
                    self.remove_widget(self.errorlab)
                except:
                    pass
            except ValueError:
                self.errorlab.text = 'Invalid, enter pOH again'
                try:
                    self.add_widget(self.errorlab)
                except:
                    pass

    def on_focus(self, instance, value, *args):
        if value:
            self.chemt.text = ''
