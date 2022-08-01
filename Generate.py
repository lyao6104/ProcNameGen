import tkinter as tk
from tkinter import filedialog

from src.names_util import *

root = tk.Tk()
root.withdraw()

# Select language file
language_path = filedialog.askopenfilename(
    title="Please select the language file.", filetypes=[("Language files", "json")], initialdir="."
)
language = load_language(language_path)

# Generate names
batch_size = int(input("Enter number of names to generate: "))
generate = True
while generate:
    print("")
    for _ in range(0, batch_size):
        print(language.get_name())
    generate = input(f"\nGenerate {batch_size} more names (Y/n)? ") != "n"
