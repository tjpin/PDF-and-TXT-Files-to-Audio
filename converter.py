import pyttsx3
import PyPDF2
import os
import random


class LoadData:
    file_text = ''

    def pdf_loader(self, file):
        data = PyPDF2.PdfFileReader(file)
        txt = []
        for i in range(data.getNumPages()):
            page = data.getPage(i)
            txt.append(page.extractText().split('\n'))
        return txt

    def text_loader(self, file, page):
        data = PyPDF2.PdfFileReader(file)
        selected_page = data.getPage(page)
        text = selected_page.extractText()
        return text


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


