import tkinter as tk
import pyautogui as auto
from decouple import config
import os

# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
os.startfile(config('GAME_PATH'))
window = tk.Tk()
window.title("Game Bot")
window.geometry('350x200')
lbl = tk.Label(window, text="Welcome")
btn = tk.Button(window, text="Exit")
lbl.grid(column=0, row=0)
btn.grid(column=1, row=0)
window.mainloop()
