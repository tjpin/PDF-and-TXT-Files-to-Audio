from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.button import ButtonBehavior
from kivymd.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
import time


from converter import LoadData, AudioConverter


class LoadPdf(BoxLayout):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class AudioWindow(BoxLayout):
    file = ''

    def __init__(self, **kwargs):
        super(AudioWindow, self).__init__(**kwargs)

        Clock.schedule_interval(self.blinker, 2)

        self.fm = None
        self.pop = None

    def blinker(self, dt=0):
        blink = self.ids.blink
        anim = Animation(size=[180, 180], t='out_quad', d=1, opacity=1) + Animation(size=[230, 230], t='out_quad', opacity=0.7, d=1)
        anim.start(blink)

    def load_pdf_file(self):
        path = r'\Users\lazar\Desktop'
        self.fm = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            search='all',
            ext=[".pdf"],
        )
        self.fm.show(path)

    def load_txt_file(self):
        path = r'\Users\lazar\Desktop'
        self.fm = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            search='all',
            ext=[".txt"],
        )
        self.fm.show(path)

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

    def text_to_audio(self):
        pass

    def complete(self, dt=0):
        self.ids.s_manager.current = 'upload'

    def pdf_to_audio(self):
        pload = LoadData()
        audio = AudioConverter()
        to_upload = pload.pdf_loader(self.file)
        start = time.time()
        audio.generate_audio(to_upload)
        finish = time.time()
        duration = finish - start
        toast(f'File saved in {self.file}')
        Clock.schedule_once(self.complete, duration)


class MainApp(MDApp):
    def build(self):
        return AudioWindow()


if __name__ == "__main__":
    MainApp().run()
