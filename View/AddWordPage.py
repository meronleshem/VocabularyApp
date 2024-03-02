import tkinter as tk


class AddWordPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Add Word Page")
        self.label.grid(row=2, column=2)

        self.word_entry = tk.Entry(self)
        self.word_entry.grid(row=3, column=2)

        self.button = tk.Button(self, text="Submit")
        self.button.grid(row=4, column=2)
