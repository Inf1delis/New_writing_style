from os import system as os
import sys
import xerox
import pynput
import random
import locale
import win32api
from platform import system


Key = pynput.keyboard.Key

print(win32api.GetKeyboardLayout())

# LANG = 'v' # АНГЛИЙСКИЙ
LANG = 'м' # РУССКИЙ

WINDOWS_MODE = system() == 'Windows'

# THERE ARE A LOT OF SHIT IN THE CODE! BE CAREFUL!
shift = Key.shift
shift_str = str(shift)
option = Key.ctrl if WINDOWS_MODE else Key.alt
left = Key.left
enter = Key.enter
ctrl = Key.ctrl if WINDOWS_MODE else Key.cmd_l
space = Key.space
space_str = str(space)
delete = Key.delete
backspace = Key.backspace
backspace_str = str(backspace)
symbols = ''.join([chr(i) for i in range(33, 65)])
symbols += ''.join([chr(i) for i in range(91, 97)])
symbols += ''.join([chr(i) for i in range(123, 127)])
vk_smiles = ['&#128127;', '&#128163;', '&#128552;', '&#128158;',
             '&#128539;', '&#128528;', '&#128580;', '&#128545;',
             '&#128169;', '&#128526;', '&#128517;', '&#128527;',
             '&#128520;', '&#128514;', '&#128133;']

also_pressed_key_en = {'-': '_', '=': '+', '`': '~', '[': '{', ']': '}', ',': '<', '.': '>', '/': '?',
                       '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*',
                       '9': '(', '0': ')'}
also_pressed_key_ru = {'-': '_', '=': '+', '`': 'Ё', '[': 'Х', ']': 'Ъ', ',': 'Б', '.': 'Ю', '/': ',',
                       '1': '!', '2': '"', '3': '№', '4': ';', '5': '%', '6': ':', '7': '?', '8': '*',
                       '9': '(', '0': ')'}
# WARNING !!!!!!!

word_buf = []
prg_exit = False
mode = False
keybrd = pynput.keyboard.Controller()
letter_counter = 0


def random_smile():
    index = random.randint(0, len(vk_smiles) - 1)
    return vk_smiles[index]


def dawn_mode(key):
    global mode
    mode = not mode
    if key[1] not in symbols:
        return key[1].upper() if mode else key[1].lower()
    else:
        return key[1]


def algorithm():
    global word_buf, letter_counter
    # word_string = ''.join([str(ch) for ch in word_buf])
    # # копируем наше слово в буфер обмена
    # xerox.copy(word_string)
    #
    # # выделяем введенное слово
    # with keybrd.pressed(shift, option):
    #     keybrd.press(left)
    #     keybrd.release(left)
    #
    #
    # with keybrd.pressed(ctrl):
    #     keybrd.press(LANG)
    #     keybrd.release(LANG)
    #
    #     if WINDOWS_MODE:  # особенность
    #         keybrd.press(delete)
    #         keybrd.release(delete)


    # ХУЯРИМ ЧЕРЕЗ БЭКСПЕЙСЫ

    for i in range(letter_counter+1):
        keybrd.press(backspace)
        keybrd.release(backspace)

    buff_length = len(word_buf)
    i = 0
    while i < buff_length:
        key_str = word_buf[i]
        if len(key_str) == 1:
            print(key_str)
            keybrd.press(key_str)
            keybrd.release(key_str)

        elif key_str == shift_str:
            try:
                while word_buf[i+1] == shift_str:
                    i += 1
                with keybrd.pressed(shift):
                    i += 1
                    key_str = word_buf[i]

                    print(key_str)
                    keybrd.press(key_str)
                    keybrd.release(key_str)
            except:
                print('idi nahui')
        i += 1

    # ставим пробел после записи
    keybrd.press(space)
    keybrd.release(space)

    # del word_string
    letter_counter = 0
    del word_buf[:]


def on_press(key):
    global word_buf, prg_exit, letter_counter, mode
    key = str(key)

    # if key[1] in symbols:
    #     pass
    #
    # elif len(key) == 3:       # отсеивает командные кнопки
    #     word_buf.append(dawn_mode(key))
    #
    # elif len(word_buf) != 0:
    #     if key == 'Key.space':
    #         word_buf.append(random_smile(vk_smiles))
    #     elif key == 'Key.backspace':
    #         word_buf.pop()

    if key == 'Key.esc':
        prg_exit = True

    elif len(key) == 3:       # отсеивает командные кнопки
        letter_counter += 1
        key_str = key[1]
        is_meta_symbol = False
        # word_buf.append(dawn_mode(key))
        mode = not mode
        if keybrd.pressed(shift) and key[1] in '-=`[],./1234567890':
            if win32api.GetKeyboardLayout() == 67699721:  # английская раскладка
                word_buf.append(also_pressed_key_en[key[1]])
                is_meta_symbol = True
            elif win32api.GetKeyboardLayout() == 68748313:  # русская раскладка 
                word_buf.append(also_pressed_key_ru[key[1]])
                is_meta_symbol = True

        if not is_meta_symbol and mode:
            word_buf.append(shift_str)

        # if key_str == '?':
        #     word_buf.append(shift_str)
        #     key_str = '7'

        if not is_meta_symbol:
            word_buf.append(key_str.lower())

    elif len(word_buf) != 0 and key == 'Key.backspace':
        word_buf.pop()
    elif key == shift_str:
        word_buf.append(key)


def on_release(key):
    if prg_exit or letter_counter != 0 and \
             (key == space or key == enter):
        return False


while True:
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()     # мониторинг клавиатуры

    print(word_buf)

    if prg_exit == True:
        del keybrd
        break

    if letter_counter != 0:
        algorithm()
