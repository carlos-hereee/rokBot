from PIL import ImageGrab
import pyautogui
import time


class Cordinates():
    init_btn = (650, 966)
    actual_size = (1600, 930)
    size_of_computer = ()


def start_game():
    pyautogui.click(Cordinates.init_btn)
    time.sleep(.2)


def find_player():
    pyautogui.click()
