from converter import AudioConverter, LoadData


def tests():
    pf = 'assets/pyjnius-latests.pdf'
    file = LoadData()
    sy = file.pdf_loader(pf)
    audio = AudioConverter()
    audio.generate_audio(sy)


tests()
