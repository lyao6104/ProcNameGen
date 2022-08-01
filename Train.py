import tkinter as tk
from tkinter import filedialog

from src.names_util import *

root = tk.Tk()
root.withdraw()

language_path = filedialog.askopenfilename(
    title="Please select the language file.", filetypes=[("Language files", "json")], initialdir="."
)
train_language(language_path)
