import re
import os
import tkinter as tk
from tkinter import filedialog

# Regex pattern for dates like: 9 March 2026
date_pattern = re.compile(r'^\d{1,2}\s+[A-Za-z]+\s+\d{4}$')

# Hide main tkinter window
root = tk.Tk()
root.withdraw()

# Ask user to select the input file
input_path = filedialog.askopenfilename(
    title="Select the input TXT file",
    filetypes=[("Text files", "*.txt")]
)

if not input_path:
    print("No file selected.")
    exit()

# Create output path in the same directory
directory = os.path.dirname(input_path)
output_path = os.path.join(directory, "cleaned_words.txt")

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8") as outfile:

    for line in infile:
        line = line.strip()

        if not line or date_pattern.match(line):
            continue

        outfile.write(line + "\n")

print("Done!")
print("Output saved to:", output_path)