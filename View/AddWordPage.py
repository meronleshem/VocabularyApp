import tkinter as tk


class AddWordPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Add Word Page")
        self.label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.word_entry = tk.Entry(self)
        self.word_entry.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        self.add_word_btn = tk.Button(self, text="Add Word")
        self.add_word_btn.grid(row=4, column=2, padx=80, pady=10, sticky="w")

        self.add_from_file_btn = tk.Button(self, text="Add Words From File")
        self.add_from_file_btn.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.translate_btn = tk.Button(self, text="Translate")
        self.translate_btn.grid(row=4, column=2, padx=10, pady=2, sticky="w")

        self.all_words_btn = tk.Button(self, text="Show All Words")
        self.all_words_btn.grid(row=7, column=2, padx=10, pady=10, sticky="w")

        self.quiz_btn = tk.Button(self, text="Quiz")
        self.quiz_btn.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.translate_word_label = tk.Label(self, text="", anchor="w", justify="left", font=("Arial", 11))
        self.translate_word_label.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.translate_word_examples = tk.Label(self, text="", anchor="w", justify="left", font=("Arial", 11))
        self.translate_word_examples.grid(row=3, column=3, padx=5, pady=5, sticky="w")
