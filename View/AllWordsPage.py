import tkinter as tk


class AllWordsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="All Words Page")
        self.label.grid(row=4, column=2)

        self.button = tk.Button(self, text="Add Word")
        self.button.grid(row=5, column=2)
