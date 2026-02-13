# """
# Quiz Setup Dialog - Configure quiz before starting
#
# Allows user to select:
# - Difficulty levels
# - Groups
# - Number of questions (optional)
# """
# import tkinter as tk
# from tkinter import ttk, simpledialog
# import ttkbootstrap as tb
# from typing import List, Dict, Optional
#
#
# class QuizSetupDialog(tk.Toplevel):
#     """
#     Modern quiz setup dialog.
#
#     Allows users to configure quiz settings before starting:
#     - Select difficulty levels
#     - Choose groups
#     - Set number of questions
#     """
#
#     def __init__(self, parent, available_groups: List[str]):
#         super().__init__(parent)
#
#         self.available_groups = available_groups
#         self.result: Optional[Dict] = None
#
#         # Configuration
#         self.title("Quiz Setup")
#         self.geometry("600x850")
#         # self.resizable(Tr, False)
#
#         # Make modal
#         self.transient(parent)
#         self.grab_set()
#
#         # Configure background
#         self.configure(bg="#e8eaf6")
#
#         # Create UI
#         self._create_header()
#         self._create_content()
#         self._create_buttons()
#
#         # Center dialog
#         self._center_dialog()
#
#         # Wait for user
#         self.wait_window()
#
#     def _create_header(self):
#         """Create dialog header."""
#         header = tk.Frame(self, bg="#3f51b5", height=70)
#         header.pack(fill="x")
#         header.pack_propagate(False)
#
#         tk.Label(header, text="🎯 Quiz Setup",
#                 font=("Segoe UI", 18, "bold"),
#                 bg="#3f51b5", fg="#ffffff").pack(side="left", padx=25, pady=20)
#
#         tk.Label(header, text="Configure your quiz",
#                 font=("Segoe UI", 10),
#                 bg="#3f51b5", fg="#e8eaf6").pack(side="left", padx=(0, 25))
#
#     def _create_content(self):
#         """Create dialog content."""
#         # Main content area
#         content = tk.Frame(self, bg="#e8eaf6")
#         content.pack(fill="both", expand=True, padx=25, pady=25)
#
#         # Difficulty section
#         self._create_difficulty_section(content)
#
#         # Groups section
#         self._create_groups_section(content)
#
#         # Question count section (optional)
#         self._create_question_count_section(content)
#
#     def _create_difficulty_section(self, parent):
#         """Create difficulty selection section."""
#         # Card
#         card = tk.Frame(parent, bg="#ffffff", relief="flat",
#                        highlightbackground="#c5cae9", highlightthickness=1)
#         card.pack(fill="x", pady=(0, 15))
#
#         # Header
#         header = tk.Frame(card, bg="#ffffff")
#         header.pack(fill="x", padx=20, pady=(15, 10))
#
#         tk.Label(header, text="📊 Difficulty Levels",
#                 font=("Segoe UI", 12, "bold"),
#                 bg="#ffffff", fg="#283593").pack(anchor="w")
#
#         tk.Label(header, text="Select which difficulty levels to include",
#                 font=("Segoe UI", 9),
#                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(3, 0))
#
#         # Checkboxes
#         checks = tk.Frame(card, bg="#ffffff")
#         checks.pack(fill="x", padx=20, pady=(0, 15))
#
#         self.diff_new = tk.IntVar(value=1)
#         self.diff_easy = tk.IntVar(value=1)
#         self.diff_medium = tk.IntVar(value=1)
#         self.diff_hard = tk.IntVar(value=1)
#
#         ttk.Checkbutton(checks, text="New Words",
#                        variable=self.diff_new).pack(anchor="w", pady=3)
#         ttk.Checkbutton(checks, text="Easy",
#                        variable=self.diff_easy).pack(anchor="w", pady=3)
#         ttk.Checkbutton(checks, text="Medium",
#                        variable=self.diff_medium).pack(anchor="w", pady=3)
#         ttk.Checkbutton(checks, text="Hard",
#                        variable=self.diff_hard).pack(anchor="w", pady=3)
#
#     def _create_groups_section(self, parent):
#         """Create groups selection section."""
#         # Card
#         card = tk.Frame(parent, bg="#ffffff", relief="flat",
#                        highlightbackground="#c5cae9", highlightthickness=1)
#         card.pack(fill="x", pady=(0, 15))
#
#         # Header
#         header = tk.Frame(card, bg="#ffffff")
#         header.pack(fill="x", padx=20, pady=(15, 10))
#
#         tk.Label(header, text="📚 Word Groups",
#                 font=("Segoe UI", 12, "bold"),
#                 bg="#ffffff", fg="#283593").pack(anchor="w")
#
#         tk.Label(header, text="Choose which groups to include in quiz",
#                 font=("Segoe UI", 9),
#                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(3, 0))
#
#         # Groups container with scroll
#         groups_container = tk.Frame(card, bg="#ffffff")
#         groups_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))
#
#         # Canvas for scrolling
#         canvas = tk.Canvas(groups_container, height=150, bg="#ffffff",
#                           highlightthickness=0)
#         scrollbar = ttk.Scrollbar(groups_container, orient="vertical",
#                                  command=canvas.yview)
#         scrollable = tk.Frame(canvas, bg="#ffffff")
#
#         scrollable.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )
#
#         canvas.create_window((0, 0), window=scrollable, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
#
#         # Group checkboxes
#         self.group_vars = {}
#
#         if self.available_groups:
#             for group in sorted(self.available_groups):
#                 var = tk.IntVar(value=1)  # All selected by default
#                 ttk.Checkbutton(scrollable, text=group,
#                                variable=var).pack(anchor="w", pady=2)
#                 self.group_vars[group] = var
#         else:
#             tk.Label(scrollable, text="No groups available",
#                     font=("Segoe UI", 10), bg="#ffffff",
#                     fg="#999").pack(pady=20)
#
#         canvas.pack(side="left", fill="both", expand=True)
#         if self.available_groups:
#             scrollbar.pack(side="right", fill="y")
#
#         # Select/Deselect buttons
#         btn_row = tk.Frame(card, bg="#ffffff")
#         btn_row.pack(fill="x", padx=20, pady=(0, 15))
#
#         tb.Button(btn_row, text="Select All", bootstyle="info-outline",
#                  width=12, command=self._select_all_groups).pack(side="left", padx=(0, 5))
#         tb.Button(btn_row, text="Deselect All", bootstyle="secondary-outline",
#                  width=12, command=self._deselect_all_groups).pack(side="left")
#
#     def _create_question_count_section(self, parent):
#         """Create question count section."""
#         # Card
#         card = tk.Frame(parent, bg="#ffffff", relief="flat",
#                        highlightbackground="#c5cae9", highlightthickness=1)
#         card.pack(fill="x")
#
#         # Header
#         header = tk.Frame(card, bg="#ffffff")
#         header.pack(fill="x", padx=20, pady=(15, 10))
#
#         tk.Label(header, text="🔢 Quiz Length",
#                 font=("Segoe UI", 12, "bold"),
#                 bg="#ffffff", fg="#283593").pack(anchor="w")
#
#         tk.Label(header, text="How many questions?",
#                 font=("Segoe UI", 9),
#                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(3, 0))
#
#         # Options
#         options = tk.Frame(card, bg="#ffffff")
#         options.pack(fill="x", padx=20, pady=(0, 15))
#
#         self.quiz_length = tk.StringVar(value="all")
#
#         ttk.Radiobutton(options, text="All available words",
#                        variable=self.quiz_length,
#                        value="all").pack(anchor="w", pady=3)
#
#         custom_row = tk.Frame(options, bg="#ffffff")
#         custom_row.pack(anchor="w", pady=3)
#
#         ttk.Radiobutton(custom_row, text="Custom:",
#                        variable=self.quiz_length,
#                        value="custom").pack(side="left")
#
#         self.custom_count = tk.IntVar(value=20)
#         ttk.Spinbox(custom_row, from_=5, to=100, width=10,
#                    textvariable=self.custom_count).pack(side="left", padx=5)
#
#         tk.Label(custom_row, text="questions", bg="#ffffff",
#                 font=("Segoe UI", 9), fg="#666").pack(side="left")
#
#     def _create_buttons(self):
#         """Create action buttons."""
#         btn_frame = tk.Frame(self, bg="#e8eaf6")
#         btn_frame.pack(fill="x", padx=25, pady=(0, 25))
#
#         tb.Button(btn_frame, text="Cancel", bootstyle="secondary",
#                  width=15, command=self._on_cancel).pack(side="right", padx=(10, 0))
#
#         tb.Button(btn_frame, text="Start Quiz →", bootstyle="success",
#                  width=15, command=self._on_start).pack(side="right")
#
#     def _select_all_groups(self):
#         """Select all groups."""
#         for var in self.group_vars.values():
#             var.set(1)
#
#     def _deselect_all_groups(self):
#         """Deselect all groups."""
#         for var in self.group_vars.values():
#             var.set(0)
#
#     def _on_start(self):
#         """Handle Start Quiz button."""
#         # Collect settings
#         difficulties = []
#         if self.diff_new.get():
#             difficulties.append("NEW_WORD")
#         if self.diff_easy.get():
#             difficulties.append("EASY")
#         if self.diff_medium.get():
#             difficulties.append("MEDIUM")
#         if self.diff_hard.get():
#             difficulties.append("HARD")
#
#         # Check if at least one difficulty selected
#         if not difficulties:
#             tk.messagebox.showwarning(
#                 "No Difficulty Selected",
#                 "Please select at least one difficulty level.",
#                 parent=self
#             )
#             return
#
#         # Collect selected groups
#         selected_groups = [
#             group for group, var in self.group_vars.items()
#             if var.get() == 1
#         ]
#
#         # Get question count
#         if self.quiz_length.get() == "all":
#             question_count = None  # All questions
#         else:
#             question_count = self.custom_count.get()
#
#         # Set result
#         self.result = {
#             "difficulties": difficulties,
#             "groups": selected_groups if selected_groups else None,
#             "question_count": question_count
#         }
#
#         self.destroy()
#
#     def _on_cancel(self):
#         """Handle Cancel button."""
#         self.result = None
#         self.destroy()
#
#     def _center_dialog(self):
#         """Center dialog on parent."""
#         self.update_idletasks()
#         parent = self.master
#
#         x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
#         y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
#
#         self.geometry(f"+{x}+{y}")


"""
Quiz Setup Dialog - Compact Horizontal Design

Modern, space-efficient layout with sections side-by-side.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import ttkbootstrap as tb
from typing import List, Dict, Optional


class QuizSetupDialog(tk.Toplevel):
    """
    Compact quiz setup dialog with horizontal layout.

    Features:
    - Three sections side-by-side
    - Minimal vertical space
    - Modern card design
    - Easy to scan
    """

    def __init__(self, parent, available_groups: List[str]):
        super().__init__(parent)

        self.available_groups = available_groups
        self.result: Optional[Dict] = None

        # Configuration
        self.title("Quiz Setup")
        self.geometry("850x500")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Configure background
        self.configure(bg="#e8eaf6")

        # Create UI
        self._create_header()
        self._create_content()
        self._create_buttons()

        # Center dialog
        self._center_dialog()

        # Wait for user
        self.wait_window()

    def _create_header(self):
        """Create compact header."""
        header = tk.Frame(self, bg="#3f51b5", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg="#3f51b5")
        header_content.pack(fill="both", expand=True, padx=20, pady=12)

        tk.Label(header_content, text="🎯 Quiz Setup",
                 font=("Segoe UI", 16, "bold"),
                 bg="#3f51b5", fg="#ffffff").pack(side="left")

        tk.Label(header_content, text="Configure your quiz settings",
                 font=("Segoe UI", 9),
                 bg="#3f51b5", fg="#e8eaf6").pack(side="left", padx=(15, 0))

    def _create_content(self):
        """Create horizontal layout with three columns."""
        # Main content area
        content = tk.Frame(self, bg="#e8eaf6")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Configure grid for 3 columns
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=1)

        # Three columns
        self._create_difficulty_column(content)
        self._create_groups_column(content)
        self._create_settings_column(content)

    def _create_difficulty_column(self, parent):
        """Create difficulty selection column."""
        # Card
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Header
        header = tk.Frame(card, bg="#43a047")  # Green
        header.pack(fill="x")

        tk.Label(header, text="📊 Difficulty",
                 font=("Segoe UI", 11, "bold"),
                 bg="#43a047", fg="#ffffff").pack(pady=12, padx=15)

        # Content
        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text="Select levels to include:",
                 font=("Segoe UI", 8),
                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 8))

        # Checkboxes
        self.diff_new = tk.IntVar(value=1)
        self.diff_easy = tk.IntVar(value=1)
        self.diff_medium = tk.IntVar(value=1)
        self.diff_hard = tk.IntVar(value=1)

        ttk.Checkbutton(content, text="New Words",
                        variable=self.diff_new).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Easy",
                        variable=self.diff_easy).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Medium",
                        variable=self.diff_medium).pack(anchor="w", pady=3)
        ttk.Checkbutton(content, text="Hard",
                        variable=self.diff_hard).pack(anchor="w", pady=3)

    def _create_groups_column(self, parent):
        """Create groups selection column."""
        # Card
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=1, sticky="nsew", padx=4)

        # Header
        header = tk.Frame(card, bg="#1e88e5")  # Blue
        header.pack(fill="x")

        tk.Label(header, text="📚 Groups",
                 font=("Segoe UI", 11, "bold"),
                 bg="#1e88e5", fg="#ffffff").pack(pady=12, padx=15)

        # Content
        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content, text="Choose word groups:",
                 font=("Segoe UI", 8),
                 bg="#ffffff", fg="#666").pack(anchor="w", pady=(0, 8))

        # Scrollable groups
        groups_frame = tk.Frame(content, bg="#ffffff")
        groups_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(groups_frame, height=120, bg="#ffffff",
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(groups_frame, orient="vertical",
                                  command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ffffff")

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Group checkboxes
        self.group_vars = {}

        if self.available_groups:
            for group in sorted(self.available_groups):
                var = tk.IntVar(value=1)
                ttk.Checkbutton(scrollable, text=group,
                                variable=var).pack(anchor="w", pady=2)
                self.group_vars[group] = var
        else:
            tk.Label(scrollable, text="No groups",
                     font=("Segoe UI", 9), bg="#ffffff",
                     fg="#999").pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        if self.available_groups:
            scrollbar.pack(side="right", fill="y")

        # Quick buttons
        if self.available_groups:
            btn_row = tk.Frame(content, bg="#ffffff")
            btn_row.pack(fill="x", pady=(8, 0))

            tb.Button(btn_row, text="All", bootstyle="info-outline",
                      width=8, command=self._select_all_groups).pack(side="left", padx=(0, 4))
            tb.Button(btn_row, text="None", bootstyle="secondary-outline",
                      width=8, command=self._deselect_all_groups).pack(side="left")

    def _create_settings_column(self, parent):
        """Create settings column."""
        # Card
        card = tk.Frame(parent, bg="#ffffff", relief="flat",
                        highlightbackground="#c5cae9", highlightthickness=1)
        card.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        # Header
        header = tk.Frame(card, bg="#fb8c00")  # Orange
        header.pack(fill="x")

        tk.Label(header, text="⚙️ Settings",
                 font=("Segoe UI", 11, "bold"),
                 bg="#fb8c00", fg="#ffffff").pack(pady=12, padx=15)

        # Content
        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Quiz length
        tk.Label(content, text="Quiz Length:",
                 font=("Segoe UI", 10, "bold"),
                 bg="#ffffff", fg="#283593").pack(anchor="w", pady=(0, 8))

        self.quiz_length = tk.StringVar(value="all")

        ttk.Radiobutton(content, text="All words",
                        variable=self.quiz_length,
                        value="all").pack(anchor="w", pady=4)

        custom_row = tk.Frame(content, bg="#ffffff")
        custom_row.pack(anchor="w", pady=4)

        ttk.Radiobutton(custom_row, text="Limit to:",
                        variable=self.quiz_length,
                        value="custom").pack(side="left")

        self.custom_count = tk.IntVar(value=20)
        ttk.Spinbox(custom_row, from_=5, to=100, width=8,
                    textvariable=self.custom_count).pack(side="left", padx=(5, 3))

        tk.Label(custom_row, text="questions", bg="#ffffff",
                 font=("Segoe UI", 8), fg="#666").pack(side="left")

        # Spacer
        tk.Frame(content, bg="#ffffff", height=15).pack()

        # Quick start option
        tk.Label(content, text="Quick Options:",
                 font=("Segoe UI", 10, "bold"),
                 bg="#ffffff", fg="#283593").pack(anchor="w", pady=(5, 8))

        tk.Frame(content, bg="#e0e0e0", height=1).pack(fill="x", pady=8)

        # Quick preset buttons
        preset_frame = tk.Frame(content, bg="#ffffff")
        preset_frame.pack(fill="x")

        tb.Button(preset_frame, text="🎯 Easy Quiz",
                  bootstyle="success-outline",
                  command=self._preset_easy).pack(fill="x", pady=2)

        tb.Button(preset_frame, text="🔥 Hard Quiz",
                  bootstyle="danger-outline",
                  command=self._preset_hard).pack(fill="x", pady=2)

        tb.Button(preset_frame, text="📝 Quick 10",
                  bootstyle="info-outline",
                  command=self._preset_quick).pack(fill="x", pady=2)

    def _create_buttons(self):
        """Create action buttons."""
        btn_frame = tk.Frame(self, bg="#e8eaf6")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Left side - info
        info_label = tk.Label(btn_frame,
                              text="💡 Tip: Select at least one difficulty level",
                              font=("Segoe UI", 8),
                              bg="#e8eaf6", fg="#666")
        info_label.pack(side="left")

        # Right side - buttons
        tb.Button(btn_frame, text="Cancel", bootstyle="secondary",
                  width=12, command=self._on_cancel).pack(side="right", padx=(8, 0))

        tb.Button(btn_frame, text="Start Quiz →", bootstyle="success",
                  width=14, command=self._on_start).pack(side="right")

    # ==================== Preset Methods ====================

    def _preset_easy(self):
        """Easy quiz preset - only new and easy words."""
        self.diff_new.set(1)
        self.diff_easy.set(1)
        self.diff_medium.set(0)
        self.diff_hard.set(0)
        self.quiz_length.set("custom")
        self.custom_count.set(15)

    def _preset_hard(self):
        """Hard quiz preset - medium and hard only."""
        self.diff_new.set(0)
        self.diff_easy.set(0)
        self.diff_medium.set(1)
        self.diff_hard.set(1)
        self.quiz_length.set("all")

    def _preset_quick(self):
        """Quick quiz preset - 10 questions, all levels."""
        self.diff_new.set(1)
        self.diff_easy.set(1)
        self.diff_medium.set(1)
        self.diff_hard.set(1)
        self.quiz_length.set("custom")
        self.custom_count.set(10)

    # ==================== Helper Methods ====================

    def _select_all_groups(self):
        """Select all groups."""
        for var in self.group_vars.values():
            var.set(1)

    def _deselect_all_groups(self):
        """Deselect all groups."""
        for var in self.group_vars.values():
            var.set(0)

    def _on_start(self):
        """Handle Start Quiz button."""
        # Collect settings
        difficulties = []
        if self.diff_new.get():
            difficulties.append("NEW_WORD")
        if self.diff_easy.get():
            difficulties.append("EASY")
        if self.diff_medium.get():
            difficulties.append("MEDIUM")
        if self.diff_hard.get():
            difficulties.append("HARD")

        # Validate
        if not difficulties:
            messagebox.showwarning(
                "No Difficulty Selected",
                "Please select at least one difficulty level.",
                parent=self
            )
            return

        # Collect groups
        selected_groups = [
            group for group, var in self.group_vars.items()
            if var.get() == 1
        ]

        # Get question count
        if self.quiz_length.get() == "all":
            question_count = None
        else:
            question_count = self.custom_count.get()

        # Set result
        self.result = {
            "difficulties": difficulties,
            "groups": selected_groups if selected_groups else None,
            "question_count": question_count
        }

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = None
        self.destroy()

    def _center_dialog(self):
        """Center dialog on parent."""
        self.update_idletasks()
        parent = self.master

        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2

        self.geometry(f"+{x}+{y}")
