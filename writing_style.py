from os import system as os
import sys
import xerox
import pynput
from gc import collect
from platform import system


Key = pynput.keyboard.Key

# LANG = 'v' # АНГЛИЙСКИЙ
LANG = 'м' # РУССКИЙ

WINDOWS_MODE = system() == 'Windows'

# THERE ARE A LOT OF SHIT IN THE CODE! BE CAREFUL!
shift = Key.shift
option = Key.ctrl if WINDOWS_MODE else Key.alt
left = Key.left
enter = Key.enter
ctrl = Key.ctrl if WINDOWS_MODE else Key.cmd_l
space = Key.space
delete = Key.delete
symbols = ',.:;<=>?@[]^-_`{"|"}§±'
symbols += ''.join([chr(i) for i in range(20, 41)])
vk_smiles = ['&#128127;', '&#128163;', '&#128552;', '&#128158;', '&#128539;', '&#128528;', '&#128580;', '&#128545;',
             '&#128169;', '&#128526;', '&#128517;', '&#128527;', '&#128520;', '&#128514;', '&#128133;']
# здесь можно конечно пробежаться в цикле for in range, но не все смайлы крутые
clear = lambda: os('cls' if WINDOWS_MODE else 'clear')
# WARNING !!!!!!!

word_buf = []
exit = False
mode = False
keybrd = pynput.keyboard.Controller()


def random_smile(smiles):
    index = random.randint(0, len(smiles) - 1)
    return vk_smiles[index]


def dawn_mode(key):
    global mode
    mode = not mode
    if key[1] not in symbols:
        return key[1].upper() if mode else key[1].lower()
    else:
        return key[1]


def algorithm():
    global word_buf
    word_string = ''.join([str(ch) for ch in word_buf])
    # копируем наше слово в буфер обмена
    xerox.copy(word_string)

    # выделяем введенное слово
    with keybrd.pressed(shift, option):
        keybrd.press(left)
        keybrd.release(left)

    with keybrd.pressed(ctrl):
        keybrd.press(LANG)
        keybrd.release(LANG)

        if WINDOWS_MODE:  # особенность
            keybrd.press(delete)
            keybrd.release(delete)
    # ставим пробел после записи
    keybrd.press(space)
    keybrd.release(space)

    del word_string
    del word_buf[:]


def on_press(key):
    global word_buf, exit
    key = str(key)

    if len(key) == 3:       # отсеивает командные кнопки
        word_buf.append(dawn_mode(key))
    elif key == 'Key.space':
        word_buf.append(random_smile(vk_smiles))
    elif len(word_buf) != 0 and key == 'Key.backspace':
        word_buf.pop()
    elif key == 'Key.esc':
        exit = True


def on_release(key):
    if exit or len(word_buf) != 0 and \
             (key == space or key == enter):
        return False


while True:
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()     # мониторинг клавиатуры
        del listener

    if exit == True:
        sys.exit()
    algorithm()
    collect()       # зовет сборщик мусора
    clear()         # очищает консоль
