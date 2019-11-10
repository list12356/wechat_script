import time
import sys
import os

from pynput import keyboard
from pynput.mouse import Button, Controller
import ctypes

from utils.screen import get_gender
from utils.constant import MALE, FEMALE

# windows api scaling
errocode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

# TODO: use config file
MOUSE_PRIMARY = Button.right
MOUSE_SECONDARY = Button.left
mouse = Controller()
VERBOSE = True
DEBUG = False

def on_press(key):
    pass

def on_release_start(key):
    try:
        if key == keyboard.Key.f6:
            return False
    except:
        pass


def on_release_exit(key):
    try:
        if key == keyboard.Key.esc:
            os._exit(1)
    except:
        pass
    try:
        if key.char == 'q':
            os._exit(1) 
    except:
        pass

def click(x, y):
    mouse.position = (x, y)
    mouse.press(MOUSE_PRIMARY)
    time.sleep(0.1)
    mouse.release(MOUSE_PRIMARY)

def perform_action():
    count_male = 0
    count_female = 0
    x = 520
    y = 147
    # hardcode on number of row
    for row in range(15):
        # hard code to handle window popup
        for col in range(12):
            click(x, y)
            time.sleep(0.2)
            gender = get_gender(x, y)
            if gender == MALE:
                count_male += 1
            elif gender == FEMALE:
                count_female += 1
            click(x, y)
            x += 84
        # window will pop up on left
        for col in range(4):
            click(x, y)
            time.sleep(0.2)
            gender = get_gender(x - 369, y)
            if gender == MALE:
                count_male += 1
            elif gender == FEMALE:
                count_female += 1
            click(x, y)
            x += 84
        
        x = 520
        # here is a hard code
        if row < 9:
            mouse.scroll(0, -185)
            time.sleep(2)
        else:
            y += 130
        
        print('male: {!s}, female: {!s}'.format(count_male, count_female))
    


def main():

    with keyboard.Listener(on_press=on_press, on_release=on_release_start) as listener:
        listener.join()

    stop_listener = keyboard.Listener(on_press=on_press, on_release=on_release_exit)
    stop_listener.start()
    print("start action...")
    perform_action()

main()
    