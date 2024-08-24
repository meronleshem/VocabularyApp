import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from tkinter import simpledialog


class GroupSelectionDialog(simpledialog.Dialog):
    def __init__(self, parent, groups):
        self.groups = groups
        self.group_vars = {}
        super().__init__(parent, title="Select Groups")

    def body(self, master):
        for group in self.groups:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(master, text=group, variable=var)
            checkbox.pack(anchor='w')
            self.group_vars[group] = var

    def apply(self):
        self.selected_groups = [group for group, var in self.group_vars.items() if var.get()]

class DifficultyDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Choose difficulty:").pack(pady=10)

        self.result = None

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        easy_button = tb.Button(button_frame, bootstyle="success-outline-toolbutton", text="Easy", width=10, command=lambda: self.set_result("Easy"))
        easy_button.pack(side=tk.LEFT, padx=5)

        medium_button = tb.Button(button_frame,bootstyle="warning-outline-toolbutton", text="Medium", width=10, command=lambda: self.set_result("Medium"))
        medium_button.pack(side=tk.LEFT, padx=5)

        hard_button = tb.Button(button_frame,bootstyle="danger-outline-toolbutton", text="Hard", width=10, command=lambda: self.set_result("Hard"))
        hard_button.pack(side=tk.LEFT, padx=5)

    def set_result(self, value):
        self.result = value
        self.ok()

    def buttonbox(self):
        # Override this method to do nothing, effectively removing the default OK and Cancel buttons
        pass

    def apply(self):
        pass


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
        self.res_label.grid(row=8, column=2, padx=50, pady=10, sticky="w")

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

        self.update_btn = tb.Button(self, text="Update Difficulty")
        self.update_btn.grid(row=10, column=2, padx=45, pady=10, sticky="w")

        self.select_groups_btn = tk.Button(self, text="Select Groups")
        self.select_groups_btn.grid(row=11, column=2, padx=45, pady=10, sticky="w")

    def show_options(self, eng_word, heb_ans, options_list):
        self.eng_word_label.config(text=eng_word)

        self.option1_btn.config(text=options_list[0])
        self.option2_btn.config(text=options_list[1])
        self.option3_btn.config(text=options_list[2])
        self.option4_btn.config(text=options_list[3])

    def change_color(self):
        pass
