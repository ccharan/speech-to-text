# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:33:31 2021

@author: Charan C
"""

import speech_recognition as sr

file_name = 'transcibed.txt'
decision = 'None'

example_path = 'C:\\Users\\Charan\\General\\'
path = input("\nEnter the path for the file to be saved ex - [{}]: ".format(example_path))
path.replace('\\', '\\\\')

file = path + '\\' + file_name

languages = """English
Hindi
Kannada
Tamil
Telugu
"""

print('\n***Languages***')
print(languages)

lang_code_dict = {'English': 'en-IN', 'Hindi': 'hi-IN', 'Kannada': 'kn-IN', 'Tamil': 'ta-IN', 'Telugu': 'te-IN'}

while True:
    lang = input('Enter the language that you are going to speak: ')
    lang_code = lang_code_dict.get(lang)

    if lang_code in lang_code_dict.values():
        break
    print('Invalid, Try again')

r = sr.Recognizer()
mic = sr.Microphone()

while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print('start speaking')
            audio = r.listen(source)

        with open(file, mode='a', encoding='utf8', errors='ignore') as f:
            f.write(r.recognize_google(audio, language=lang_code))
            f.write('\n')
        f.close()

        decision = input('Do you want to continue? (y/n): ')
        if decision == 'y':
            continue
        elif decision == 'n':
            break
        else:
            print('Invalid input, exiting...')

    except BaseException as e:
        print(e)

print('\nRESULT: file is saved at {} as {} '.format(path.replace('\\\\', '\\'), file_name))

input('\nType any keyword to exit!!!')
