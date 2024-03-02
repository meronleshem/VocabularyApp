import tkinter as tk
from tkinter import ttk


class AllWordsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="All Words Page")
        self.label.grid(row=4, column=2)

        custom_font = ("Helvetica", 12)

        self.word_listbox = tk.Listbox(self, width=100, height=10, font=custom_font)
        self.word_listbox.grid(row=5, column=2, padx=30, pady=10)
        self.word_listbox.bind("<Double-Button-1>", self.on_double_click)

        # style = ttk.Style()
        # style.configure("Custom.Treeview", background="#f0f0f0")
        #
        # self.tree = ttk.Treeview(self, columns=("English", "Hebrew"),  style="Custom.Treeview")
        #
        # self.tree.heading("English", text="English", anchor="w")
        # self.tree.heading("Hebrew", text="Hebrew", anchor="w")
        #
        # self.tree.grid(row=5, column=2, sticky="ns")

        self.button = tk.Button(self, text="Add Word")
        self.button.grid(row=6, column=2)

    def on_double_click(self, event):
        index =  self.word_listbox.curselection()
        if index:  # Check if an item is selected
            # Get the text of the selected item
            item_text =  self.word_listbox.get(index)
            # Print the text of the selected item
            print(item_text)

    def show_words(self, word_list):
        # for eng_word, heb_word in word_list:
        #     self.tree.insert("", "end", values=(eng_word, heb_word))
        for eng_word, heb_word in word_list:
            self.word_listbox.insert(tk.END, f"{eng_word} - {heb_word}")