import tkinter as tk
from tkinter import ttk


class AllWordsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="All Words Page")
        self.label.grid(row=4, column=2)
        # Draw a rectangle on the canvas
        custom_font = ("Helvetica", 12)

       # self.word_listbox = tk.Listbox(self, width=90, height=10, font=custom_font)
       # self.word_listbox.grid(row=5, column=2, padx=30, pady=10)
       # self.word_listbox.bind("<Double-Button-1>", self.on_double_click)

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#f0f0f0")

        self.tree = ttk.Treeview(self, columns=("English", "Hebrew", "Difficulty", "Group"),  style="Custom.Treeview", show='headings')
       # self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.heading("English", text="English", anchor="w")
        self.tree.heading("Hebrew", text="Hebrew", anchor="w")
        self.tree.heading("Difficulty", text="Difficulty", anchor="w")
        self.tree.heading("Group", text="Group", anchor="w")
        self.tree.column("English", width=150)
        self.tree.column("Hebrew", width=400)
        self.tree.column("Difficulty", width=100)
        self.tree.column("Group", width=100)
        self.tree.grid(row=5, column=2, sticky="nsew")

        self.button = tk.Button(self, text="Add Word")
        self.button.grid(row=6, column=2)

        self.word_expand_label = tk.Label(self, text="")
        self.word_expand_label.grid(row=7, column=2)

    # def on_double_click(self, event):
    #     index = self.word_listbox.curselection()
    #     if index:
    #         item_text = self.word_listbox.get(index)
    #         print(item_text)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        # Do something with the values, for example print them
        print(values)

    def show_words(self, word_list):
         for eng_word, heb_word, difficulty, group_name in word_list:
             self.tree.insert("", "end", values=(eng_word, heb_word, difficulty, group_name))
        #for eng_word, heb_word in word_list:
        #    self.word_listbox.insert(tk.END, f"{eng_word} - {heb_word}")