from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.button import ButtonBehavior
from kivymd.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from threading import Thread
import time
import os
from converter import LoadData, AudioConverter


class LoadPdf(BoxLayout):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class AudioWindow(BoxLayout):
    file = ''
    fm = None
    pop = None
    path = r'\Users\<...>\Desktop'

    def __init__(self, **kwargs):
        super(AudioWindow, self).__init__(**kwargs)

        self.converted()

    def blinker(self, dt=0):
        blink = self.ids.blink
        anim = Animation(size=[180, 180], t='out_quad', d=1, opacity=1) + Animation(size=[230, 230], t='out_quad',
                                                                                    opacity=0.7, d=1)
        anim.start(blink)

    def load_pdf_file(self):
        self.fm = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            search='all',
            ext=[".pdf"],
        )
        self.fm.show(self.path)

    def load_txt_file(self):
        self.fm = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            search='all',
            ext=[".txt"],
        )
        self.fm.show(self.path)

    def loading(self):
        self.ids.s_manager.current = 'loading'

    def select_path(self, path):
        self.file = path
        _box = LoadPdf()
        _box.ids.image_path.text = path
        self.pop = Popup(
            content=_box,
            background='',
            size_hint=(0.6, 0.8))
        self.pop.open()

    def exit_manager(self, *args):
        self.fm.close()

    def complete(self, dt=0):
        self.ids.s_manager.current = 'upload'

    # @mainthread
    def document_to_audio(self):
        to_upload = None
        pload = LoadData()
        audio = AudioConverter()
        if self.file.endswith('.pdf'):
            to_upload = pload.pdf_loader(self.file)
        else:
            to_upload = pload.text_loader(self.file)
        start = time.time()
        audio.generate_audio(to_upload)
        finish = time.time()
        duration = finish - start
        toast(f'File saved in {os.getcwd()}')
        Clock.schedule_once(self.complete, duration)

    def action1(self):
        self.pop.dismiss()
        self.fm.close()
        self.loading()

    def action(self):
        self.ids.start_gen.text = "generating audio..."
        # self.ids.spin.active = True
        Clock.schedule_interval(self.blinker, 2)
        self.ids.message.text = 'This might take several minutes depending on file size'

    def converted(self):
        path = r"C:\Users\<converted files path\>"
        for b, n, p in os.walk(path):
            for m in p:
                if m.endswith(".mp3"):
                    lst = OneLineIconListItem(text=m, on_release=lambda x: toast(path))
                    img = IconLeftWidget(icon='music')
                    lst.add_widget(img)
                    self.ids.converted_list.add_widget(lst)


class MainApp(MDApp):
    def build(self):
        return AudioWindow()


if __name__ == "__main__":
    MainApp().run()
