import tkinter as tk
from tkinter import ttk


class QuizPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.eng_word_label = tk.Label(self, text="", font=("Arial", 13))
        #self.eng_word_label.grid(row=2, column=2, padx=50, pady=20, sticky="w")
        self.dummy_label = tk.Label(self, text="")
        self.dummy_label.grid(row=2, column=2, padx=50, pady=20)
        self.eng_word_label.place(x=20, y=20)

        self.choice = tk.StringVar()

        self.style = ttk.Style()
        self.style.configure("Correct.TRadiobutton", background="green", foreground="black", padding=10)
        self.style.configure("Incorrect", background="red", foreground="black", padding=10)

        self.option1 = ttk.Radiobutton(self, variable=self.choice, value=1)
        self.option2 = ttk.Radiobutton(self, variable=self.choice, value=2)
        self.option3 = ttk.Radiobutton(self, variable=self.choice, value=3)
        self.option4 = ttk.Radiobutton(self, variable=self.choice, value=4)

        self.option1.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        self.option2.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.option3.grid(row=5, column=2, padx=10, pady=10, sticky="w")
        self.option4.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        self.next_btn = tk.Button(self, text="Next")
        self.next_btn.grid(row=7, column=2, padx=120, pady=10, sticky="w")

        self.submit_btn = tk.Button(self, text="Submit Answer")
        self.submit_btn.grid(row=7, column=2, padx=20, pady=10, sticky="w")

        self.res_label = tk.Label(self, text="", font=("Arial", 15))
        self.res_label.grid(row=8, column=2, padx=50, pady=20, sticky="w")

    def show_options(self, eng_word, heb_ans, options_list):
        self.eng_word_label.config(text=eng_word)

        self.option1.config(text=options_list[0], value=options_list[0])
        self.option2.config(text=options_list[1], value=options_list[1])
        self.option3.config(text=options_list[2], value=options_list[2])
        self.option4.config(text=options_list[3], value=options_list[3])

    def change_color(self):
        pass
