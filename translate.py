import speech_recognition as sr
from utils import dct, button_status


def main(lan):
    r = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            dct["STATE"] = True
            audio = r.listen(source)
            print(r.recognize_google(audio, language=lan))
            dct["STATE"] = False
            button_status["button"] = True
    except BaseException as e:
        print(e)

