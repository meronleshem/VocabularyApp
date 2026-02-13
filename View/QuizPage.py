# import tkinter as tk
# from tkinter import ttk
# import ttkbootstrap as tb
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
            checkbox.pack(anchor="w")
            self.group_vars[group] = var

    def apply(self):
        self.selected_groups = [
            group for group, var in self.group_vars.items() if var.get()
        ]


class DifficultyDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Choose difficulty:", font=("Arial", 12)).pack(pady=10)

        self.result = None

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        tb.Button(
            button_frame,
            bootstyle="success-outline",
            text="Easy",
            width=10,
            command=lambda: self.set_result("Easy"),
        ).pack(side=tk.LEFT, padx=5)

        tb.Button(
            button_frame,
            bootstyle="warning-outline",
            text="Medium",
            width=10,
            command=lambda: self.set_result("Medium"),
        ).pack(side=tk.LEFT, padx=5)

        tb.Button(
            button_frame,
            bootstyle="danger-outline",
            text="Hard",
            width=10,
            command=lambda: self.set_result("Hard"),
        ).pack(side=tk.LEFT, padx=5)

    def set_result(self, value):
        self.result = value
        self.ok()

    def buttonbox(self):
        pass


class QuizPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Layout config
        self.grid_columnconfigure(2, weight=1)

        # ===== HEADER BAR =====
        header = tk.Frame(self, bg="#f8f9fa")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header.grid_columnconfigure(1, weight=1)
        self.back_btn = tb.Button(
            header,
            text="←",
            width=3,
            bootstyle="primary",
        )
        self.back_btn.grid(row=0, column=0, sticky="w")
        # Word label
        self.eng_word_label = tb.Label(
            self,
            text="",
            font=("Arial", 18, "bold"),
            wraplength=700,
            justify="center",
        )
        self.eng_word_label.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="ew")

        # Answer buttons (fixed layout)
        self.option_frames = []
        self.option_buttons = []

        for i in range(4):
            frame = tk.Frame(self, height=90)
            frame.grid(row=1 + i, column=2, padx=20, pady=6, sticky="ew")
            frame.grid_propagate(False)

            btn = tk.Button(
                frame,
                text="",
                font=("Arial", 12),
                wraplength=650,
                justify="left",
                anchor="w",
                padx=12,
                pady=8,
                relief="raised",
            )
            btn.pack(fill="both", expand=True)

            self.option_frames.append(frame)
            self.option_buttons.append(btn)

        # Next button
        self.next_btn = tb.Button(
            self, text="Next", bootstyle="primary", width=12
        )
        self.next_btn.grid(row=6, column=2, padx=20, pady=(10, 5), sticky="w")

        # Result label
        self.res_label = tb.Label(self, text="", font=("Arial", 14))
        self.res_label.grid(row=7, column=2, padx=20, pady=5, sticky="w")

        # Difficulty filters
        self.choice_new = tk.IntVar(value=1)
        self.choice_easy = tk.IntVar(value=1)
        self.choice_medium = tk.IntVar(value=1)
        self.choice_hard = tk.IntVar(value=1)

        filters_frame = tk.Frame(self)
        filters_frame.grid(row=8, column=2, padx=20, pady=10, sticky="w")

        ttk.Checkbutton(filters_frame, text="New", variable=self.choice_new).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(filters_frame, text="Easy", variable=self.choice_easy).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(filters_frame, text="Medium", variable=self.choice_medium).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(filters_frame, text="Hard", variable=self.choice_hard).pack(side=tk.LEFT, padx=5)

        # Action buttons
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=9, column=2, padx=20, pady=(5, 20), sticky="w")

        self.update_btn = tb.Button(actions_frame, text="Update Difficulty")
        self.update_btn.pack(side=tk.LEFT, padx=5)
        self.select_groups_btn = tb.Button(actions_frame, text="Select Groups")
        self.select_groups_btn.pack(side=tk.LEFT, padx=5)

        self.progress_label = tb.Label(
            actions_frame,
            text="0 of 0",
            font=("Segoe UI", 10),
            bootstyle="secondary",
        )
        self.progress_label.pack(pady=(4, 0))

    def show_options(self, eng_word, heb_ans, options_list):
        self.eng_word_label.config(text=eng_word)

        for btn, text in zip(self.option_buttons, options_list):
            btn.config(text=text)

    def reset_button_colors(self):
        for btn in self.option_buttons:
            btn.config(bg="SystemButtonFace", fg="black")

    def update_progress(self, current, total):
        self.progress_label.config(text=f"{current} of {total}")
