import tkinter as tk
from tkinter import filedialog

from src.names_util import *

# Not withdrawing the window, otherwise the second file dialog doesn't appear.
root = tk.Tk()

# Get some basic information
names_path = filedialog.askopenfilename(
    title="Please select your list of names.", initialdir="."
)
order = int(input("Enter the order (1-3): "))
if order < 1:
    order = 1
elif order > 3:
    order = 3
language_name = input("Enter the name of your language: ")
if not language_name:
    language_name = "Unnamed Language"

# Scan the provided names file
language = scan_names(names_path, order, language_name)
language_destination = filedialog.askdirectory(
    title="Please select a location to save the new language.", initialdir="."
)
save_language(f"{language_destination}/{language.name}.json", language, True)
