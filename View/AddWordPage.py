import tkinter as tk


class AddWordPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Add Word Page")
        self.label.grid(row=0, column=2, padx=10, pady=10, sticky="we")

        self.word_entry = tk.Entry(self)
        self.word_entry.grid(row=1, column=2, padx=10, pady=10, sticky="we")

        self.add_word_btn = tk.Button(self, text="Add Word")
        self.add_word_btn.grid(row=4, column=2, padx=80, pady=10, sticky="w")

        self.add_from_text_file_btn = tk.Button(self, text="Add Words From Text File")
        self.add_from_text_file_btn.grid(row=5, column=2, padx=10, pady=10, sticky="we")

        self.add_from_pdf_btn = tk.Button(self, text="Add Words From PDF")
        self.add_from_pdf_btn.grid(row=6, column=2, padx=10, pady=10, sticky="we")

        self.translate_btn = tk.Button(self, text="Translate")
        self.translate_btn.grid(row=4, column=2, padx=10, pady=2, sticky="e")

        self.all_words_btn = tk.Button(self, text="Show All Words")
        self.all_words_btn.grid(row=7, column=2, padx=10, pady=10, sticky="we")

        self.quiz_btn = tk.Button(self, text="Quiz")
        self.quiz_btn.grid(row=8, column=2, padx=10, pady=10, sticky="we")

        self.translate_frame = tk.Frame(parent, background="blue")
        self.translate_frame.grid(row=0, column=2)

        self.translate_word_label = tk.Label(self.translate_frame, text="", anchor="w", justify="left", font=("Arial", 11))
        self.translate_word_label.grid(row=1, column=0, pady=5, sticky="we")

        self.translate_word_examples = tk.Label(self.translate_frame, text="", anchor="w", justify="left", font=("Arial", 11))
        self.translate_word_examples.grid(row=4, column=0, pady=5, sticky="we")
