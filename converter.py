import pyttsx3
import PyPDF2
import os
import random


class LoadData:

    text = []

    def pdf_loader(self, file):
        data = PyPDF2.PdfFileReader(file)

        for i in range(data.getNumPages()):
            page = data.getPage(i)
            self.text.append(page.extractText().split('\n'))
        return self.text

    def text_loader(self, file):
        with open(file, 'r') as f:
            for txt in f.readlines():
                self.text.append(txt.split('\n'))
        return self.text



class AudioConverter:

    def generate_audio(self, text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 150)

        counter = random.randrange(1, 1000)
        filename = 'audio book'
        if os.path.exists(filename):
            engine.save_to_file(text, f'{filename + str(counter)}.mp3', os.getcwd())
            engine.runAndWait()
        else:
            engine.save_to_file(text, f'{filename + str(counter)}.mp3')
            engine.runAndWait()


