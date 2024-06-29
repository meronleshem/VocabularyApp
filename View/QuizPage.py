import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


class QuizPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.dummy_label = tk.Label(self, text="")
        self.dummy_label.grid(row=2, column=2, padx=50, pady=20)

        self.eng_word_label = tb.Label(self, text="", font=("Arial", 15))
        self.eng_word_label.place(x=200, y=20)

        self.choice = tk.StringVar()

        self.style = ttk.Style()
        self.style.configure("Correct.TRadiobutton", background="green", foreground="black", padding=10)
        self.style.configure("Incorrect", background="red", foreground="black", padding=10)

        self.option1_btn = ttk.Button(self)
        self.option2_btn = ttk.Button(self)
        self.option3_btn = ttk.Button(self)
        self.option4_btn = ttk.Button(self)

        self.option1_btn.grid(row=3, column=2, padx=10, pady=10, sticky="we")
        self.option2_btn.grid(row=4, column=2, padx=10, pady=10, sticky="we")
        self.option3_btn.grid(row=5, column=2, padx=10, pady=10, sticky="we")
        self.option4_btn.grid(row=6, column=2, padx=10, pady=10, sticky="we")

        self.next_btn = tk.Button(self, text="Next")
        self.next_btn.grid(row=7, column=2, padx=10, pady=10, sticky="w")

        self.res_label = tb.Label(self, text="", font=("Arial", 15))
        self.res_label.grid(row=8, column=2, padx=50, pady=20, sticky="w")

        self.choice_new = tk.IntVar(value=1)
        self.choice_easy = tk.IntVar(value=1)
        self.choice_medium = tk.IntVar(value=1)
        self.choice_hard = tk.IntVar(value=1)

        self.check_boxes_frame = tk.Frame()
        self.check_boxes_frame.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

        self.check_easy = ttk.Checkbutton(self, text="New", variable=self.choice_new)
        self.check_easy.grid(row=9, column=2, padx=10, pady=10, sticky="w")
        self.check_easy = ttk.Checkbutton(self, text="Easy", variable=self.choice_easy)
        self.check_easy.grid(row=9, column=2, padx=70, pady=10, sticky="w")
        self.check_medium = ttk.Checkbutton(self, text="Medium", variable=self.choice_medium)
        self.check_medium.grid(row=9, column=2, padx=130, pady=10, sticky="w")
        self.check_hard = ttk.Checkbutton(self, text="Hard", variable=self.choice_hard)
        self.check_hard.grid(row=9, column=2, padx=210, pady=10, sticky="w")

        self.difficulty_choice = tk.StringVar(value="")
        self.easy_btn = tb.Radiobutton(self, bootstyle="success-outline-toolbutton", variable=self.difficulty_choice
                                       , value="Easy", text="Easy")
        self.easy_btn.grid(row=10, column=2, padx=10, pady=10, sticky="w")
        self.medium_btn = tb.Radiobutton(self, bootstyle="warning-outline-toolbutton", variable=self.difficulty_choice
                                         , value="Medium", text="Medium")
        self.medium_btn.grid(row=10, column=2, padx=70, pady=10, sticky="w")
        self.hard_btn = tb.Radiobutton(self, bootstyle="danger-outline-toolbutton", variable=self.difficulty_choice
                                         , value="Hard", text="Hard")
        self.hard_btn.grid(row=10, column=2, padx=150, pady=10, sticky="w")

        self.update_btn = tb.Button(self, text="Update Difficulty")
        self.update_btn.grid(row=11, column=2, padx=45, pady=10, sticky="w")

    def show_options(self, eng_word, heb_ans, options_list):
        self.eng_word_label.config(text=eng_word)

        self.option1_btn.config(text=options_list[0])
        self.option2_btn.config(text=options_list[1])
        self.option3_btn.config(text=options_list[2])
        self.option4_btn.config(text=options_list[3])

    def change_color(self):
        pass
