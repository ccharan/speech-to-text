import queue
import PySimpleGUI as sg
import threading
from translate import main
from utils import dct, button_status


BG_COLOR1 = "#F4F6F2"
BG_COLOR2 = '#F4F6F2'
TXT_COLOR = '#344259'
TXT_SIZE = (20, 10)
gui_queue = queue.Queue()
mic_on = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADYElEQVR4Xq2WzWsTQRTAc1NBvQmKN1FvCsVm09BDQzZFgwoKVqvWi9jagyj6H1T8wFIPCtpWYw/2oogHPYoUxY/WItJahaJiaeoHbfGgO7v53IzzXpJt82Z2u03z4Edm5r1572W+9gUCPuVPPLSeRbWjhq7dZbo2Ktpz4jeLFNujRjR0x9BDrfONjevo/Krln65tF87vCUwB9wnYJv42h7ZRf76Fh8NrmB7qEY5yigB+gRXq5pHIaurfUyBzsawTCodVIbZt2Ny9axONoxQzVl9X2lPJ0QqZESu6k8arkNI/9xd8bxM32w4i0Jb0amZYJLiRxkWBfRIGY4pJEpmBXs7zee6IaGcStyQ7F97D+aLxA6UDR40lrI42zguFheBlEWNW+zHJXoWhB7sqgpeumq/Tnr7WRUM7Ajpqr8LUNaNiK1jxnkuGKtI9l2hcR0BH7d0wo9ptDI4v3DIemVolIGD4YsLzqlC6UsME4CwcCZTedknpRo0T6If9H6UKL2qbgDYMCcxTxWJS5zu5deak0/ebgHX2FE9d6JT8EWYhgYxC4WBPT3H7+zen7zcBmANzqT9CeskE8hNjvMAMzmIN2E93X6RxHQEdzhO2BdPk+fEPkj8CJuC5BdmHg+gclhT6ni9hx3G0SZ1rx6Hsg/uSPwJugechtE6fQOf5kdfOWGagj3PbXggO3wLxfSjr8+/elBJqk/wtBg8hlFFUQcm9eI5xMv03nDFzXxMmB0C7PJ7pv4m2uaFnkh+KSKAvADUcVVDMAzq3fyTRcfbJI+zLNjGee/oYbeyZaaUNxYhqLYG5SGSt6DCqpJgtcW5//ogBCpbFc6+GeHYwgUAbxkDyn8a5eWiPNF8Bg9jlj1FCYSDT3MDT1y9z++skBnNE7Lf9ZbJ4DUu3ZSlg652vIVZCxQJSMnQDlrjw+xfiZ7kJmZRev8VJAEQMdisMPbGTUwgdX5Jo6GpFcBAoyeBaSMYeVJOAiPGWx7euovFRoEoRRkk6yQ2zdT9Cx90J/rSi4c00boVA6cywhKaTV0ySxcI7aDylGPG6DWLCS4WTqoBldy3H3QT2CapX5uON8EB86IJXXPfcj0DmUEAuMxEG1Y501VYi8GpBDQfvN4tpIyLIbPEfIrMwZsS0XiMWPOy8cD7kP99MrQ64uF84AAAAAElFTkSuQmCC'
mic_off = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA7AAAAOwBeShxvQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAMkSURBVFiFvdfdi5dVEAfwjz+q1XWtFNM1zNp1LSlr6yqoO7tILcikICq6682/oCsDQbLbMnpdqMA1Am8Cg0K2SKIXqK1uEzZX6MUba39mbuRuFzM/+rE+Pc/59bJfODdzZubMM2fOd+ZZohwrcDe2YhTX4PLc+xlT+BoTOIJ2idMlBTrrsAePoB8z+AoncSp11mI9bslAz2Icz+J4SSBVWIa9OINZvIZt6Kux6cP21J3F79jfYFOJEXyDORzEUK8OMCyyMIePRZaKcDN+End4zz84eCF2pq9pbGlSHsnDp3Hjf3B4BzelzxNqMrFMpL1dcPjFeBJv5HoiZU1BtMV1VNbEXpzXnPZVmMQ8fsw1jy+wssH2XlETzyzcWCeq/WCDA3gTv+HOLtm2lL1eYH9IvJCN3cIXU9hU7Zek3nMVewdwTvNVDKePVzqCFfhVvN0mrBHp3l2xtzv31hT4GRMZH2gJeu3H4QLDDnPOV+zNL9Cpw2Esx46W4PYZweGLhQnxIu5oicYyKe5lsXAOn2O0JQrv+0U8vINvMdTCpQ0BXI0fsLkH55vTZkONzmlc1ipw1o9B0SPagkjWV+hdlXszoi0Ppm0tWmlwZY3OlHimt4k+fxSPYVOXzqaUvS8I6fa0marxuxK/wGf4sCHQQyJlqwSRnMpg3st1VjSxIawWE9J4g8+j+IRgpBn1Q8MNonLfwUWCbF7Al7kO4ArBgkdS9/oaf0vFdb4EDwgS2d4Q8ePijidwbcX+dSKTc3i0wdddeeb99EbFD4v0/oGP8HyuYyk7jYcK/IyJDCzvCF4VRDRcYDyIp/Fp2syKu9yjbOzamDYvdwtHxADZVDgL8UGuXvCWqJELOu9+cX87/8cAduUZ+6o2+8S41BbjUwnuy1WC0fR9TMwVlVgrhsfpHoIoPfwkvlMwL2zJANpihvu32CWGjxOCT4qw2l9v+m1RpL1ig6j083r8MemgT0yvnac2hh2Cxf4OS1NnrMtun5o7LxmfhvEUHhTEcUZwwHHZTMRf8ghuxUDqjIuXVdeQigLoYEB83VbRmodc+Hs+Kaj6XcGujfgTEirJJgxWui8AAAAASUVORK5CYII='

sg.theme(BG_COLOR1)

languages = ('English', 'Hindi', 'Kannada', 'Tamil', 'Telugu')
languages_code = ('en-IN', 'hi-IN', 'kn-IN', 'ta-IN', 'te-IN')
dict_languages = dict(zip(languages, languages_code))


left_element = [
    [sg.Text(background_color=BG_COLOR2)],
    [sg.Text("Select Language", pad=((10, 10), (0, 0)), background_color=BG_COLOR2, text_color=TXT_COLOR),
     sg.Combo(values=languages, default_value='English', readonly=False, k='LANGUAGE',
              expand_x=True, pad=((10, 10), (0, 0)), background_color=BG_COLOR2, text_color=TXT_COLOR), sg.Push(background_color=BG_COLOR2)],

    [sg.Text(background_color=BG_COLOR2)],
    [sg.Button('', image_data=mic_off, button_color=('white', BG_COLOR2), mouseover_colors=('white', BG_COLOR2),
               key='MIC', pad=(0, 0), expand_x=True)],

    [sg.Text("Transcribed Text", pad=((10, 10), (0, 0)), background_color=BG_COLOR2, text_color=TXT_COLOR)],
    [sg.Multiline(expand_y=True, expand_x=True, pad=((10, 10), (0, 0)), background_color='white',write_only=True,
                  reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, text_color=TXT_COLOR,
                  autoscroll=True, auto_refresh=True, key='LOG')],
    [sg.Text(background_color=BG_COLOR2)]
]


layout = [[sg.Column(left_element, expand_x=True, expand_y=True, background_color=BG_COLOR2)],
          [sg.Push(background_color=BG_COLOR2),
           sg.InputText("", do_not_clear=False, visible=False, key="SAVE_LOG", enable_events=True),
           sg.FileSaveAs("Save", button_color=('white', TXT_COLOR), size=(10, 1)),
           sg.Push(background_color=BG_COLOR2)]
          ]


window = sg.Window("Speech-to-Text", layout,
                   finalize=True, size=(500, 500), resizable=True,
                   background_color=BG_COLOR2)


def long_operation_thread(mic, gui_queue):
    main(mic)
    gui_queue.put(None)


def long_operation_mic(gui_queue):
    while True:
        if dct["STATE"]:
            window["MIC"].update(image_data=mic_on)
        elif button_status['button']:
            button_status['button'] = False
            window["MIC"].update(image_data=mic_off)
            break
        gui_queue.put(None)


while True:
    event, values = window.Read(timeout=100)
    if event == sg.WIN_CLOSED:
        break

    if event == 'MIC':
        mic = dict_languages[values['LANGUAGE']]
        threading.Thread(target=long_operation_thread, args=(mic, gui_queue,), daemon=True).start()
        threading.Thread(target=long_operation_mic, args=(gui_queue,), daemon=True).start()
    elif event == "SAVE_LOG":
        log_file = values['SAVE_LOG']
        with open(log_file, mode='w', encoding='UTF-8') as file:
            file.write(window['LOG'].get())

    try:
        message = gui_queue.get_nowait()
    except queue.Empty:
        message = None

    if message:
        print('Got a message back from the thread: ', message)

window.close()
