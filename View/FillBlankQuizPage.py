import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from typing import List


class FillBlankQuizPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#e8eaf6")

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create UI
        self._create_header()
        self._create_quiz_area()
        self._create_control_panel()

        # Variables for tracking
        self.answer_selected = False

    def _create_header(self):
        """Create header with title and progress."""
        header = tk.Frame(self, bg="#5e35b1", height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.columnconfigure(1, weight=1)

        # Back button
        self.back_btn = tb.Button(header, text="← Back",
                                  bootstyle="light-outline", width=10)
        self.back_btn.grid(row=0, column=0, padx=20, pady=15)

        # Title
        tk.Label(header, text="📝 Fill in the Blank Quiz",
                 font=("Segoe UI", 16, "bold"),
                 bg="#5e35b1", fg="#ffffff").grid(row=0, column=1, sticky="w", padx=20)

        # Progress
        self.progress_label = tk.Label(header, text="Question 0/0",
                                       font=("Segoe UI", 11),
                                       bg="#5e35b1", fg="#e8eaf6")
        self.progress_label.grid(row=0, column=2, padx=20)

        # Difficulty badge
        self.diff_badge = tk.Label(header, text="NEW",
                                   font=("Segoe UI", 9, "bold"),
                                   bg="#757575", fg="#ffffff",
                                   padx=10, pady=3)
        self.diff_badge.grid(row=0, column=3, padx=(0, 20))

    def _create_quiz_area(self):
        """Create quiz area with sentence and options."""
        quiz_container = tk.Frame(self, bg="#e8eaf6")
        quiz_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        quiz_container.columnconfigure(0, weight=1)
        quiz_container.rowconfigure(0, weight=1)

        # Content frame
        content = tk.Frame(quiz_container, bg="#e8eaf6")
        content.grid(row=0, column=0)
        content.columnconfigure(0, weight=1)

        # Sentence card
        sentence_card = tk.Frame(content, bg="#ffffff", relief="flat",
                                 highlightbackground="#c5cae9", highlightthickness=1)
        sentence_card.grid(row=0, column=0, sticky="ew", pady=(0, 30))

        sentence_content = tk.Frame(sentence_card, bg="#ffffff")
        sentence_content.pack(fill="both", padx=30, pady=30)

        tk.Label(sentence_content, text="Complete the sentence:",
                 font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 15))

        # Sentence with blank
        self.sentence_label = tk.Label(
            sentence_content,
            text="The quick brown fox jumps over the _____ dog.",
            font=("Segoe UI", 16),
            bg="#ffffff",
            fg="#283593",
            wraplength=600,
            justify="left"
        )
        self.sentence_label.pack(anchor="w")

        # Instructions
        tk.Label(content, text="Select the correct word to fill in the blank:",
                 font=("Segoe UI", 10, "bold"),
                 bg="#e8eaf6", fg="#5e35b1").grid(row=1, column=0, sticky="w", pady=(0, 15))

        # Answer buttons
        self.option_buttons = []
        for i in range(4):
            btn = tb.Button(
                content,
                text="Option",
                bootstyle="outline-primary",
                width=40
            )
            btn.grid(row=2 + i, column=0, sticky="ew", pady=5)
            self.option_buttons.append(btn)

        # Result label
        self.res_label = tk.Label(
            content,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg="#e8eaf6"
        )
        self.res_label.grid(row=6, column=0, pady=(20, 0))

        # Next button
        self.next_btn = tb.Button(
            content,
            text="Next Question →",
            bootstyle="success",
            width=25,
            state="disabled"
        )
        self.next_btn.grid(row=7, column=0, pady=(15, 0))

    def _create_control_panel(self):
        """Create bottom control panel."""
        control = tk.Frame(self, bg="#ffffff", height=60)
        control.grid(row=2, column=0, sticky="ew")
        control.grid_propagate(False)

        # Left side - filters
        left = tk.Frame(control, bg="#ffffff")
        left.pack(side="left", padx=30, pady=15)

        tk.Label(left, text="Difficulty Filters:",
                 font=("Segoe UI", 9, "bold"),
                 bg="#ffffff").pack(side="left", padx=(0, 10))

        self.choice_new = tk.IntVar(value=1)
        self.choice_easy = tk.IntVar(value=1)
        self.choice_medium = tk.IntVar(value=1)
        self.choice_hard = tk.IntVar(value=1)

        ttk.Checkbutton(left, text="New", variable=self.choice_new).pack(side="left", padx=5)
        ttk.Checkbutton(left, text="Easy", variable=self.choice_easy).pack(side="left", padx=5)
        ttk.Checkbutton(left, text="Medium", variable=self.choice_medium).pack(side="left", padx=5)
        ttk.Checkbutton(left, text="Hard", variable=self.choice_hard).pack(side="left", padx=5)

        # Divider
        tk.Frame(control, bg="#e0e0e0", width=1).pack(side="left", fill="y", padx=20, pady=10)

        # Right side - actions & stats
        right = tk.Frame(control, bg="#ffffff")
        right.pack(side="left", pady=15)

        self.select_groups_btn = tb.Button(right, text="📚 Select Groups",
                                           bootstyle="info-outline", width=15)
        self.select_groups_btn.pack(side="left", padx=5)

        self.new_quiz_btn = tb.Button(right, text="🔄 New Quiz",
                                      bootstyle="primary-outline", width=15)
        self.new_quiz_btn.pack(side="left", padx=5)

        # Stats
        stats = tk.Frame(control, bg="#f5f5f5", relief="flat",
                         highlightbackground="#c5cae9", highlightthickness=1)
        stats.pack(side="right", padx=30, pady=10)

        self.stats_label = tk.Label(stats, text="✓ 0  ✗ 0  📊 0%",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#f5f5f5", fg="#5e35b1")
        self.stats_label.pack(padx=15, pady=8)

    # ==================== Update Methods ====================

    def show_sentence(self, sentence: str):
        """Display sentence with blank."""
        self.sentence_label.config(text=sentence)

    def show_options(self, options: List[str]):
        """Display answer options and enable buttons."""
        for i, (btn, option) in enumerate(zip(self.option_buttons, options)):
            btn.config(
                text=option,
                state="normal",
                bootstyle="outline-primary"
            )
            # Don't override command - it's already bound by controller
        self.answer_selected = False

    def highlight_answer(self, button_index: int, is_correct: bool):
        """Highlight selected answer with visual indicator."""
        btn = self.option_buttons[button_index]
        current_text = btn.cget("text")

        # Disable the button
        btn.config(state="disabled")

        # Add visual indicator to text
        if is_correct:
            btn.config(text=f"✓ {current_text}")
            try:
                btn.config(bootstyle="success")
            except:
                pass
        else:
            btn.config(text=f"✗ {current_text}")
            try:
                btn.config(bootstyle="danger")
            except:
                pass

    def show_result(self, is_correct: bool, correct_word: str = None, hebrew_word: str = None):
        """Show result message with Hebrew translation and enable next button."""
        if is_correct:
            if hebrew_word:
                self.res_label.config(
                    text=f"✓ Correct! ({hebrew_word})",
                    fg="#43a047"
                )
            else:
                self.res_label.config(text="✓ Correct!", fg="#43a047")
        else:
            if correct_word and hebrew_word:
                self.res_label.config(
                    text=f"✗ Incorrect. The answer was: {correct_word} ({hebrew_word})",
                    fg="#e53935"
                )
            elif correct_word:
                self.res_label.config(
                    text=f"✗ Incorrect. The answer was: {correct_word}",
                    fg="#e53935"
                )
            else:
                self.res_label.config(text="✗ Incorrect", fg="#e53935")

        # Enable next button
        self.next_btn.config(state="normal")

    def reset_button_colors(self):
        """Reset all buttons to default style."""
        for btn in self.option_buttons:
            btn.config(bootstyle="outline-primary", state="normal")

    def update_progress(self, current: int, total: int):
        """Update progress label."""
        self.progress_label.config(text=f"Question {current}/{total}")

    def update_difficulty_badge(self, difficulty: str):
        """Update difficulty badge."""
        colors = {
            "NEW_WORD": ("#757575", "NEW"),
            "EASY": ("#43a047", "EASY"),
            "MEDIUM": ("#fb8c00", "MED"),
            "HARD": ("#e53935", "HARD")
        }

        color, text = colors.get(difficulty, ("#757575", "NEW"))
        self.diff_badge.config(text=text, bg=color)

    def update_stats(self, correct: int, wrong: int):
        """Update statistics display."""
        total = correct + wrong
        accuracy = (correct / total * 100) if total > 0 else 0
        self.stats_label.config(text=f"✓ {correct}  ✗ {wrong}  📊 {accuracy:.0f}%")

    def enable_next_button(self):
        """Enable the next button."""
        self.next_btn.config(state="normal")

    def disable_next_button(self):
        """Disable the next button."""
        self.next_btn.config(state="disabled")