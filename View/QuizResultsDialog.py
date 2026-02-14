"""
"""
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from typing import List, Tuple


class QuizResultsDialog(tk.Toplevel):
    """
    Quiz results dialog - shows score and ALL mistakes.
    """

    def __init__(self, parent, correct: int, wrong: int, mistakes: List[Tuple[str, str, str]]):
        """
        Initialize results dialog.

        Args:
            parent: Parent widget
            correct: Number of correct answers
            wrong: Number of wrong answers
            mistakes: List of (english_word, user_answer, correct_answer) tuples
        """
        super().__init__(parent)

        self.correct = correct
        self.wrong = wrong
        self.total = correct + wrong
        self.mistakes = mistakes
        self.action = None

        # Configuration
        self.title("Quiz Complete!")
        self.geometry("950x750")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Configure background
        self.configure(bg="#e8eaf6")

        # Create UI
        self._create_header()
        self._create_score_section()
        self._create_mistakes_section()
        self._create_buttons()

        # Center dialog
        self._center_dialog()

        # Debug print
        print(f"Dialog created with {len(mistakes)} mistakes")
        for m in mistakes:
            print(f"  - {m}")

        # Wait for user
        self.wait_window()

    def _create_header(self):
        """Create header."""
        accuracy = (self.correct / self.total * 100) if self.total > 0 else 0

        if accuracy >= 90:
            bg_color = "#43a047"
            emoji = "🎉"
            title = "Excellent!"
        elif accuracy >= 70:
            bg_color = "#1e88e5"
            emoji = "👍"
            title = "Great Job!"
        elif accuracy >= 50:
            bg_color = "#fb8c00"
            emoji = "💪"
            title = "Good Effort!"
        else:
            bg_color = "#e53935"
            emoji = "📚"
            title = "Keep Learning!"

        header = tk.Frame(self, bg=bg_color, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=f"{emoji} {title}",
                 font=("Segoe UI", 18, "bold"),
                 bg=bg_color, fg="#ffffff").pack(pady=20, padx=25)

    def _create_score_section(self):
        """Create score summary."""
        score_frame = tk.Frame(self, bg="#ffffff")
        score_frame.pack(fill="x", padx=25, pady=20)

        # Stats row
        stats = tk.Frame(score_frame, bg="#ffffff")
        stats.pack(pady=20)

        # Correct
        tk.Label(stats, text=str(self.correct), font=("Segoe UI", 36, "bold"),
                 bg="#ffffff", fg="#43a047").pack(side="left", padx=30)
        tk.Label(stats, text="Correct", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666").pack(side="left", padx=(0, 50))

        # Wrong
        tk.Label(stats, text=str(self.wrong), font=("Segoe UI", 36, "bold"),
                 bg="#ffffff", fg="#e53935").pack(side="left", padx=30)
        tk.Label(stats, text="Wrong", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666").pack(side="left", padx=(0, 50))

        # Accuracy
        accuracy = (self.correct / self.total * 100) if self.total > 0 else 0
        tk.Label(stats, text=f"{accuracy:.0f}%", font=("Segoe UI", 36, "bold"),
                 bg="#ffffff", fg="#1e88e5").pack(side="left", padx=30)
        tk.Label(stats, text="Accuracy", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666").pack(side="left")

    def _create_mistakes_section(self):
        """Create mistakes list - ALWAYS SHOWS."""
        container = tk.Frame(self, bg="#e8eaf6")
        container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Card
        card = tk.Frame(container, bg="#ffffff", relief="solid", borderwidth=1)
        card.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(card, bg="#ffffff")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(header, text=f"❌ Your Mistakes ({len(self.mistakes)})",
                 font=("Segoe UI", 13, "bold"),
                 bg="#ffffff", fg="#e53935").pack(side="left")

        # ALWAYS show mistakes section
        if len(self.mistakes) == 0:
            # Perfect score
            perfect = tk.Frame(card, bg="#e8f5e9")
            perfect.pack(fill="both", expand=True, padx=20, pady=30)

            tk.Label(perfect, text="🌟 Perfect Score! 🌟",
                     font=("Segoe UI", 16, "bold"),
                     bg="#e8f5e9", fg="#2e7d32").pack(pady=10)
            tk.Label(perfect, text="You got every question correct!",
                     font=("Segoe UI", 11),
                     bg="#e8f5e9", fg="#666").pack()
        else:
            # Show mistakes list
            list_frame = tk.Frame(card, bg="#ffffff")
            list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            # Canvas for scrolling
            canvas = tk.Canvas(list_frame, bg="#ffffff", highlightthickness=0, height=350)
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable = tk.Frame(canvas, bg="#ffffff")

            scrollable.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Add each mistake
            for i, (english, user_ans, correct_ans) in enumerate(self.mistakes):
                self._create_mistake_item(scrollable, i + 1, english, user_ans, correct_ans)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

    def _create_mistake_item(self, parent, number: int, english: str,
                             user_ans: str, correct_ans: str):
        """Create a mistake item."""
        # Item frame
        item = tk.Frame(parent, bg="#fff3e0", relief="solid", borderwidth=1)
        item.pack(fill="x", pady=6, padx=5)

        content = tk.Frame(item, bg="#fff3e0")
        content.pack(fill="x", padx=15, pady=12)

        # Word with number
        word_row = tk.Frame(content, bg="#fff3e0")
        word_row.pack(fill="x", pady=(0, 8))

        tk.Label(word_row, text=f"{number}.",
                 font=("Segoe UI", 11, "bold"),
                 bg="#fff3e0", fg="#e65100").pack(side="left", padx=(0, 5))

        tk.Label(word_row, text=english,
                 font=("Segoe UI", 13, "bold"),
                 bg="#fff3e0", fg="#1565c0").pack(side="left")

        # User's wrong answer
        wrong_row = tk.Frame(content, bg="#fff3e0")
        wrong_row.pack(fill="x", pady=3)

        tk.Label(wrong_row, text="Your answer:",
                 font=("Segoe UI", 9),
                 bg="#fff3e0", fg="#666").pack(side="left", padx=(0, 8))

        tk.Label(wrong_row, text=user_ans,
                 font=("Segoe UI", 11, "bold"),
                 bg="#fff3e0", fg="#c62828").pack(side="left", padx=(0, 8))

        tk.Label(wrong_row, text="✗",
                 font=("Segoe UI", 12),
                 bg="#fff3e0", fg="#c62828").pack(side="left")

        # Correct answer
        correct_row = tk.Frame(content, bg="#fff3e0")
        correct_row.pack(fill="x", pady=3)

        tk.Label(correct_row, text="Correct answer:",
                 font=("Segoe UI", 9),
                 bg="#fff3e0", fg="#666").pack(side="left", padx=(0, 8))

        tk.Label(correct_row, text=correct_ans,
                 font=("Segoe UI", 11, "bold"),
                 bg="#fff3e0", fg="#2e7d32").pack(side="left", padx=(0, 8))

        tk.Label(correct_row, text="✓",
                 font=("Segoe UI", 12),
                 bg="#fff3e0", fg="#2e7d32").pack(side="left")

    def _create_buttons(self):
        """Create action buttons."""
        btn_frame = tk.Frame(self, bg="#e8eaf6")
        btn_frame.pack(fill="x", padx=25, pady=(0, 25))

        # Close button
        tb.Button(btn_frame, text="Close", bootstyle="secondary",
                  width=12, command=self._on_close).pack(side="left")

        # New Quiz button
        tb.Button(btn_frame, text="🔄 New Quiz", bootstyle="success",
                  width=15, command=self._on_new_quiz).pack(side="right")

    def _on_close(self):
        """Close dialog."""
        self.action = None
        self.destroy()

    def _on_new_quiz(self):
        """Start new quiz."""
        self.action = "new_quiz"
        self.destroy()

    def _center_dialog(self):
        """Center dialog on parent."""
        self.update_idletasks()
        parent = self.master

        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2

        self.geometry(f"+{x}+{y}")
