import tkinter as tk
from tkinter import filedialog

from src.names_util import *
from src.util import clamp

root = tk.Tk()
root.withdraw()

# Get number of names per line
print("Enter the number of names to generate per line.")
print("This can be used to generate, for example, full names, including middle names.")
names_per_line_temp = int(input("Enter number of names per line (1-5): "))
names_per_line = clamp(names_per_line_temp, 1, 5)

# Select language file
languages = []
for _ in range(0, names_per_line):
    language_path = filedialog.askopenfilename(
        title="Please select the language file.",
        filetypes=[("Language files", "json")],
        initialdir=".",
    )
    languages.append(load_language(language_path))

# Generate names
batch_size = int(input("Enter number of names to generate: "))
generate = True
while generate:
    print("")
    for _ in range(0, batch_size):
        for i in range(0, names_per_line):
            print(languages[i].get_name(), end="")
            if i < names_per_line - 1:
                print(" ", end="")
            else:
                print("")
    generate = input(f"\nGenerate {batch_size} more names (Y/n)? ") != "n"
