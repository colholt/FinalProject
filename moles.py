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


class Element():
    def __init__(self, molar, given, atoms):
        self.molar = molar
        self.moles = float(molar) / float(given)
        self.num = 6.022e23
        self.molecules = self.num * self.moles
        self.atoms = atoms

    def result(self):
        print('Moles = ' + str(self.moles))
        print('molecules = ' + str(self.molecules))
        print('atoms = ' + str(self.molecules * self.atoms))


def ask(a, b, c):
    ele = Element(a, int(b), int(c))
    ele.result()

fs = []
for elements in pt.elements:
    fs.append(elements)

fu = []

for twi in fs:
    fu.append(str(twi))

rar = dict(zip(fu, fs))

#dz = input('enter element(s) separated by space')

#ci = dz.split()

total = 0
'''
for y in ci:
    print(rar[y].name + ': ' + str(rar[y].mass))
    total += rar[y].mass
'''
print('total = ' + str(total))


def has_num(nu):
    return any(z.isdigit() for z in nu)


class WaFF(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(BoxLayout, self).__init__(*args, **kwargs)
        self.textinput = TextInput(text='Enter elements separated by spaces', multiline=False,
                                   size=(300, 50))
        self.rut = Label(text='', pos=(450, 250))
        self.add_widget(self.textinput)
        self.textinput.bind(on_text_validate=self.chicken)
        self.wextinput = TextInput(text='Enter given', multiline=False, size=(300, 50))
        self.wextinput.bind(on_text_validate=self.alfredo)
        self.wextinput.bind(focus=self.on_focus2)
        self.reset = TextInput(text='Type reset to reset', multiline=False, size=(300, 50))
        self.texts = [self.textinput, self.wextinput, self.reset]
        self.textinput.bind(focus=self.on_focus)
        self.reset.bind(on_text_validate=self.resets)
        self.given = 0
        self.atoms = 0
        self.but = Label(text='Given: ' + str(self.given), pos=(425, 200))
        self.tut = Label(text='' + str(self.atoms), pos=(425, 225))
        self.mmlabel = Label(pos=((self.textinput.x + 50), (self.textinput.y + 100)))
        self.atlabel = Label(pos=(350, 425))
        self.molabel = Label(pos=(350, 400))
        self.tolabel = Label(pos=(350, 450))
        self.errorlabel = Label(pos=((self.textinput.x + 100), (self.textinput.y + 100)))
        self.add_widget(self.but)
        self.add_widget(self.tut)
        self.add_widget(self.atlabel)
        self.add_widget(self.molabel)
        self.add_widget(self.tolabel)
        self.mm = []

    def chicken(self, *args):
        msg = self.textinput.text
        ci = msg.split()
        tos = 0
        try:
            self.remove_widget(self.textinput)
        except:
            pass
        try:
            self.add_widget(self.wextinput)
        except:
            pass
        a = Button(text='Calculate', pos=(600, 150), background_color=(.5, .2, .5, 1))
        a.bind(on_release=partial(self.currentValue, self.calc(ci)))
        self.add_widget(a)

    def alfredo(self, *args):
        try:
            float(self.wextinput.text)
            self.given = self.wextinput.text
            self.but.text = 'Given: ' + str(self.given)
            self.wextinput.text = 'Enter atoms'
            self.wextinput.unbind(on_text_validate=self.alfredo)
        except ValueError:
            self.wextinput.text = 'Enter given'

    def calc(self, alist):
        try:
            wnum = []
            for i in alist:
                if has_num(i):
                    wnum.append(i)
                else:
                    wnum.append(i + '1')
            intel = 0
            for i in wnum:
                if len(i) == 2:
                    intel += (float(rar[i[0]].mass) * float(i[1]))
                elif len(i) == 3:
                    if i[1].isdigit():
                        intel += float(rar[i[0]].mass) * float(i[1] + i[2])
                    else:
                        intel += float(rar[i[0] + i[1]].mass) * float(i[2])
            self.mmlabel.text = 'molar mass: ' + str(intel)
            self.add_widget(self.mmlabel)
            try:
                self.remove_widget(self.errorlabel)
            except:
                pass
            return intel
        except KeyError:
            self.errorlabel.text = 'Invalid input, enter elements again'
            try:
                self.add_widget(self.errorlabel)
            except:
                pass
            try:
                self.remove_widget(self.wextinput)
                self.add_widget(self.textinput)
            except:
                pass

    def currentValue(self, x, *args):
        ele = Element(x, self.given, self.atoms)
        atoms = float(ele.atoms) * float(ele.molecules)
        self.atlabel.text = 'atoms: ' + str(atoms)
        self.molabel.text = 'molecules: ' + str(ele.molecules)
        self.tolabel.text = 'moles: ' + str(ele.moles)
        self.remove_widget(self.wextinput)
        try:
            self.add_widget(self.reset)
        except:
            pass

    def resets(self, *args):
        self.clear_widgets()
        try:
            self.add_widget(self.textinput)
        except:
            pass
        self.textinput.bind(on_text_validate=self.chicken)
        self.given = 0
        self.atoms = 0
        self.reset.unbind(on_text_validate=self.resets)
        self.add_widget(self.but)
        self.add_widget(self.tut)
        self.but.text = 'Given: ' + str(self.given)
        self.tut.text = 'Atoms: ' + str(self.atoms)

    def on_focus(self, instance, value, *args):
        if value:
            self.textinput.text = ''

    def on_focus2(self, instance, value, *args):
        if value:
            self.wextinput.text = ''