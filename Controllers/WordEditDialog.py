# """
# Word Edit Dialog - Dialog for editing word properties
#
# This module provides a dialog window for editing word difficulty, group, and examples.
# """
# import tkinter as tk
# from tkinter import ttk
# from typing import Optional, Tuple, List
# from Utils.SoundUtil import play_sound
#
#
# class WordEditDialog(tk.Toplevel):
#     """
#     Dialog for editing word properties (difficulty, group, and examples).
#
#     Features:
#     - Change difficulty level
#     - Change/update group
#     - Edit example sentences
#     - Preview current values
#     - Cancel or save changes
#
#     Attributes:
#         result: Tuple of (difficulty, group, examples) or None if cancelled
#     """
#
#     # Difficulty options
#     DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"]
#
#     def __init__(self, parent: tk.Widget, word_data: Tuple,
#                  available_groups: Optional[List[str]] = None):
#         """
#         Initialize the word edit dialog.
#
#         Args:
#             parent: Parent widget
#             word_data: Tuple of (english, hebrew, difficulty, group, examples)
#             available_groups: List of existing groups for dropdown
#         """
#         super().__init__(parent)
#
#         self.result: Optional[Tuple[str, str, str]] = None  # (difficulty, group, examples)
#         self.word_data = word_data
#         self.available_groups = available_groups or []
#
#         # Extract word information
#         self.english = word_data[0] if len(word_data) > 0 else ""
#         self.hebrew = word_data[1] if len(word_data) > 1 else ""
#         self.current_difficulty = word_data[2] if len(word_data) > 2 else "Medium"
#         self.current_group = word_data[3] if len(word_data) > 3 else ""
#         self.current_examples = word_data[4] if len(word_data) > 4 else ""
#
#         # Configure dialog
#         self.title("Edit Word")
#         self.geometry("550x750")  # Larger to fit examples
#         self.resizable(False, False)
#
#         # Make dialog modal
#         self.transient(parent)
#         self.grab_set()
#
#         # Create UI
#         self._create_widgets()
#
#         # Center dialog
#         self._center_dialog()
#
#         # Set focus
#         self.difficulty_var.set(self.current_difficulty)
#
#         # Wait for dialog to close
#         self.wait_window()
#
#     def _create_widgets(self) -> None:
#         """Create all dialog widgets."""
#         # Main container with padding
#         main_frame = ttk.Frame(self, padding="20")
#         main_frame.pack(fill="both", expand=True)
#
#         # Title
#         title_label = ttk.Label(
#             main_frame,
#             text="Edit Word Properties",
#             font=("Segoe UI", 14, "bold")
#         )
#         title_label.pack(pady=(0, 20))
#
#         # Word information section
#         self._create_word_info_section(main_frame)
#
#         # Separator
#         ttk.Separator(main_frame, orient="horizontal").pack(
#             fill="x", pady=20
#         )
#
#         # Edit section
#         self._create_edit_section(main_frame)
#
#         # Buttons
#         self._create_button_section(main_frame)
#
#     def _create_word_info_section(self, parent: ttk.Frame) -> None:
#         """Create section showing word information."""
#         info_frame = ttk.LabelFrame(
#             parent,
#             text="Word Information",
#             padding="10"
#         )
#         info_frame.pack(fill="x", pady=(0, 10))
#
#         # English word
#         english_frame = ttk.Frame(info_frame)
#         english_frame.pack(fill="x", pady=5)
#
#         ttk.Label(
#             english_frame,
#             text="English:",
#             font=("Segoe UI", 10, "bold"),
#             width=12,
#             anchor="w"
#         ).pack(side="left")
#
#         ttk.Label(
#             english_frame,
#             text=self.english,
#             font=("Segoe UI", 10)
#         ).pack(side="left")
#
#         # Hebrew word
#         hebrew_frame = ttk.Frame(info_frame)
#         hebrew_frame.pack(fill="x", pady=5)
#
#         ttk.Label(
#             hebrew_frame,
#             text="Hebrew:",
#             font=("Segoe UI", 10, "bold"),
#             width=12,
#             anchor="w"
#         ).pack(side="left")
#
#         ttk.Label(
#             hebrew_frame,
#             text=self.hebrew,
#             font=("Segoe UI", 10)
#         ).pack(side="left")
#
#     def _create_edit_section(self, parent: ttk.Frame) -> None:
#         """Create section for editing properties."""
#         edit_frame = ttk.LabelFrame(
#             parent,
#             text="Edit Properties",
#             padding="10"
#         )
#         edit_frame.pack(fill="both", expand=True)
#
#         # Difficulty section
#         self._create_difficulty_selector(edit_frame)
#
#         # Group section
#         self._create_group_selector(edit_frame)
#
#         # Examples section
#         self._create_examples_editor(edit_frame)
#
#     def _create_difficulty_selector(self, parent: ttk.Frame) -> None:
#         """Create difficulty selection section."""
#         difficulty_container = ttk.Frame(parent)
#         difficulty_container.pack(fill="x", pady=(0, 15))
#
#         # Label
#         ttk.Label(
#             difficulty_container,
#             text="Difficulty:",
#             font=("Segoe UI", 10, "bold")
#         ).pack(anchor="w", pady=(0, 8))
#
#         # Radio buttons
#         self.difficulty_var = tk.StringVar(value=self.current_difficulty)
#
#         for difficulty in self.DIFFICULTY_OPTIONS:
#             rb = ttk.Radiobutton(
#                 difficulty_container,
#                 text=difficulty,
#                 value=difficulty,
#                 variable=self.difficulty_var
#             )
#             rb.pack(anchor="w", pady=2)
#
#     def _create_group_selector(self, parent: ttk.Frame) -> None:
#         """Create group selection/input section."""
#         group_container = ttk.Frame(parent)
#         group_container.pack(fill="x", pady=(0, 10))
#
#         # Label
#         label_frame = ttk.Frame(group_container)
#         label_frame.pack(fill="x", pady=(0, 8))
#
#         ttk.Label(
#             label_frame,
#             text="Group:",
#             font=("Segoe UI", 10, "bold")
#         ).pack(side="left")
#
#         ttk.Label(
#             label_frame,
#             text="(Select existing or type new)",
#             font=("Segoe UI", 8),
#             foreground="gray"
#         ).pack(side="left", padx=(5, 0))
#
#         # Combobox (allows both selection and typing)
#         self.group_var = tk.StringVar(value=self.current_group)
#         self.group_combobox = ttk.Combobox(
#             group_container,
#             textvariable=self.group_var,
#             values=self.available_groups,
#             font=("Segoe UI", 10)
#         )
#         self.group_combobox.pack(fill="x")
#
#         # Add placeholder if empty
#         if not self.current_group:
#             self.group_combobox.insert(0, "Enter or select group...")
#             self.group_combobox.configure(foreground="gray")
#             self.group_combobox.bind("<FocusIn>", self._clear_group_placeholder)
#             self.group_combobox.bind("<FocusOut>", self._restore_group_placeholder)
#
#     def _clear_group_placeholder(self, event: tk.Event) -> None:
#         """Clear group placeholder on focus."""
#         if self.group_combobox.get() == "Enter or select group...":
#             self.group_combobox.delete(0, tk.END)
#             self.group_combobox.configure(foreground="black")
#
#     def _restore_group_placeholder(self, event: tk.Event) -> None:
#         """Restore group placeholder if empty."""
#         if not self.group_combobox.get():
#             self.group_combobox.insert(0, "Enter or select group...")
#             self.group_combobox.configure(foreground="gray")
#
#     def _create_examples_editor(self, parent: ttk.Frame) -> None:
#         """Create examples editor section."""
#         examples_container = ttk.Frame(parent)
#         examples_container.pack(fill="both", expand=True, pady=(15, 0))
#
#         # Label
#         label_frame = ttk.Frame(examples_container)
#         label_frame.pack(fill="x", pady=(0, 8))
#
#         ttk.Label(
#             label_frame,
#             text="Examples:",
#             font=("Segoe UI", 10, "bold")
#         ).pack(side="left")
#
#         ttk.Label(
#             label_frame,
#             text="(Enter example sentences using this word)",
#             font=("Segoe UI", 8),
#             foreground="gray"
#         ).pack(side="left", padx=(5, 0))
#
#         # Text widget with scrollbar
#         text_frame = ttk.Frame(examples_container)
#         text_frame.pack(fill="both", expand=True)
#
#         # Scrollbar
#         scrollbar = ttk.Scrollbar(text_frame)
#         scrollbar.pack(side="right", fill="y")
#
#         # Text widget
#         self.examples_text = tk.Text(
#             text_frame,
#             height=8,
#             width=50,
#             font=("Segoe UI", 10),
#             wrap="word",
#             yscrollcommand=scrollbar.set
#         )
#         self.examples_text.pack(side="left", fill="both", expand=True)
#         scrollbar.config(command=self.examples_text.yview)
#
#         # Insert current examples
#         if self.current_examples:
#             self.examples_text.insert("1.0", self.current_examples)
#         else:
#             # Placeholder
#             self.examples_text.insert("1.0", "Enter example sentences here...")
#             self.examples_text.configure(foreground="gray")
#             self.examples_text.bind("<FocusIn>", self._clear_examples_placeholder)
#             self.examples_text.bind("<FocusOut>", self._restore_examples_placeholder)
#
#     def _clear_examples_placeholder(self, event: tk.Event) -> None:
#         """Clear examples placeholder on focus."""
#         if self.examples_text.get("1.0", "end-1c") == "Enter example sentences here...":
#             self.examples_text.delete("1.0", "end")
#             self.examples_text.configure(foreground="black")
#
#     def _restore_examples_placeholder(self, event: tk.Event) -> None:
#         """Restore examples placeholder if empty."""
#         if not self.examples_text.get("1.0", "end-1c").strip():
#             self.examples_text.delete("1.0", "end")
#             self.examples_text.insert("1.0", "Enter example sentences here...")
#             self.examples_text.configure(foreground="gray")
#
#     def _create_button_section(self, parent: ttk.Frame) -> None:
#         """Create button section."""
#         button_frame = ttk.Frame(parent)
#         button_frame.pack(fill="x", pady=(20, 0))
#
#         # Cancel button
#         cancel_btn = ttk.Button(
#             button_frame,
#             text="Cancel",
#             command=self._on_cancel,
#             width=12
#         )
#         cancel_btn.pack(side="right", padx=(10, 0))
#
#         # Save button
#         save_btn = ttk.Button(
#             button_frame,
#             text="Save Changes",
#             command=self._on_save,
#             width=12
#         )
#         save_btn.pack(side="right")
#
#         sound_btn = ttk.Button(
#             button_frame,
#             text="Play Sound",
#             command=self._sound,
#             width=12
#         )
#         sound_btn.pack(side="right")
#
#         # Bind Enter key to save
#         self.bind("<Return>", lambda e: self._on_save())
#         self.bind("<Escape>", lambda e: self._on_cancel())
#
#     def _center_dialog(self) -> None:
#         """Center the dialog on parent window."""
#         self.update_idletasks()
#
#         # Get parent position
#         parent = self.master
#         parent_x = parent.winfo_rootx()
#         parent_y = parent.winfo_rooty()
#         parent_width = parent.winfo_width()
#         parent_height = parent.winfo_height()
#
#         # Get dialog size
#         dialog_width = self.winfo_width()
#         dialog_height = self.winfo_height()
#
#         # Calculate position
#         x = parent_x + (parent_width - dialog_width) // 2
#         y = parent_y + (parent_height - dialog_height) // 2
#
#         self.geometry(f"+{x}+{y}")
#
#     def _on_save(self) -> None:
#         """Handle save button click."""
#         # Get values
#         difficulty = self.difficulty_var.get()
#         group = self.group_var.get().strip()
#
#         # Get examples
#         examples = self.examples_text.get("1.0", "end-1c").strip()
#
#         # Check if examples is placeholder
#         if examples == "Enter example sentences here...":
#             examples = ""
#
#         # Check if group is placeholder
#         if group == "Enter or select group...":
#             group = ""
#
#         # Validate
#         if not difficulty:
#             difficulty = "Medium"
#
#         # Set result (difficulty, group, examples)
#         self.result = (difficulty, group, examples)
#
#         # Close dialog
#         self.destroy()
#
#     def _on_cancel(self) -> None:
#         """Handle cancel button click."""
#         self.result = None
#         self.destroy()
#
#     def _sound(self) -> None:
#         play_sound(self.english)
#
#
# # ==================== Alternative: Simple Menu Dialog ====================
#
# class WordActionDialog(tk.Toplevel):
#     """
#     Simple menu-based dialog for word actions.
#
#     Provides quick access to:
#     - Change difficulty
#     - Change group
#     - Delete word (optional)
#     """
#
#     def __init__(self, parent: tk.Widget, word_data: Tuple):
#         """
#         Initialize action dialog.
#
#         Args:
#             parent: Parent widget
#             word_data: Tuple of (english, hebrew, difficulty, group)
#         """
#         super().__init__(parent)
#
#         self.result: Optional[Tuple[str, any]] = None  # (action, value)
#         self.word_data = word_data
#
#         # Extract word info
#         self.english = word_data[0] if len(word_data) > 0 else ""
#         self.hebrew = word_data[1] if len(word_data) > 1 else ""
#
#         # Configure dialog
#         self.title("Word Actions")
#         self.geometry("400x850")
#         self.resizable(False, False)
#
#         # Make modal
#         self.transient(parent)
#         self.grab_set()
#
#         # Create UI
#         self._create_widgets()
#         self._center_dialog()
#
#         self.wait_window()
#
#     def _create_widgets(self) -> None:
#         """Create dialog widgets."""
#         main_frame = ttk.Frame(self, padding="20")
#         main_frame.pack(fill="both", expand=True)
#
#         # Title
#         title = ttk.Label(
#             main_frame,
#             text=f"Actions for: {self.english}",
#             font=("Segoe UI", 11, "bold")
#         )
#         title.pack(pady=(0, 20))
#
#         # Action buttons
#         btn_width = 20
#
#         change_diff_btn = ttk.Button(
#             main_frame,
#             text="Change Difficulty",
#             command=self._change_difficulty,
#             width=btn_width
#         )
#         change_diff_btn.pack(pady=5)
#
#         change_group_btn = ttk.Button(
#             main_frame,
#             text="Change Group",
#             command=self._change_group,
#             width=btn_width
#         )
#         change_group_btn.pack(pady=5)
#
#         ttk.Separator(main_frame, orient="horizontal").pack(
#             fill="x", pady=15
#         )
#
#         cancel_btn = ttk.Button(
#             main_frame,
#             text="Cancel",
#             command=self.destroy,
#             width=btn_width
#         )
#         cancel_btn.pack(pady=5)
#
#         # Bind Escape
#         self.bind("<Escape>", lambda e: self.destroy())
#
#     def _change_difficulty(self) -> None:
#         """Open difficulty change dialog."""
#         self.result = ("difficulty", None)
#         self.destroy()
#
#     def _change_group(self) -> None:
#         """Open group change dialog."""
#         self.result = ("group", None)
#         self.destroy()
#
#     def _center_dialog(self) -> None:
#         """Center dialog on parent."""
#         self.update_idletasks()
#         parent = self.master
#         x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
#         y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
#         #self.geometry(f"+{x}+{y}")
#
#
# # ==================== Usage Example ====================
#
# if __name__ == "__main__":
#     """Test the dialogs."""
#
#     root = tk.Tk()
#     root.geometry("400x300")
#     root.title("Dialog Test")
#
#
#     def test_edit_dialog():
#         word_data = ("hello", "שלום", "Medium", "Greetings", "Hello there! How are you?")
#         available_groups = ["Greetings", "Animals", "Food", "Colors", "Numbers"]
#
#         dialog = WordEditDialog(root, word_data, available_groups)
#
#         if dialog.result:
#             difficulty, group, examples = dialog.result
#             print(f"New difficulty: {difficulty}")
#             print(f"New group: {group}")
#             print(f"New examples: {examples}")
#         else:
#             print("Cancelled")
#
#
#     def test_action_dialog():
#         word_data = ("hello", "שלום", "Medium", "Greetings")
#         dialog = WordActionDialog(root, word_data)
#
#         if dialog.result:
#             action, value = dialog.result
#             print(f"Action selected: {action}")
#         else:
#             print("Cancelled")
#
#
#     # Test buttons
#     ttk.Button(
#         root,
#         text="Test Edit Dialog",
#         command=test_edit_dialog
#     ).pack(pady=20)
#
#     ttk.Button(
#         root,
#         text="Test Action Dialog",
#         command=test_action_dialog
#     ).pack(pady=10)
#
#     root.mainloop()


"""
Word Edit Dialog - Dialog for editing word properties

This module provides a dialog window for editing word difficulty and group.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, List
from Utils.SoundUtil import play_sound


class WordEditDialog(tk.Toplevel):
    """
    Dialog for editing word properties (difficulty and group).

    Features:
    - Change difficulty level
    - Change/update group
    - Preview current values
    - Cancel or save changes

    Attributes:
        result: Tuple of (difficulty, group) or None if cancelled
    """

    # Difficulty options
    DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"]

    def __init__(self, parent: tk.Widget, word_data: Tuple,
                 available_groups: Optional[List[str]] = None):
        """
        Initialize the word edit dialog.

        Args:
            parent: Parent widget
            word_data: Tuple of (english, hebrew, difficulty, group, examples)
            available_groups: List of existing groups for dropdown
        """
        super().__init__(parent)

        self.result: Optional[Tuple[str, str, str]] = None  # (difficulty, group, examples)
        self.word_data = word_data
        self.available_groups = available_groups or []

        # Extract word information
        self.english = word_data[0] if len(word_data) > 0 else ""
        self.hebrew = word_data[1] if len(word_data) > 1 else ""
        self.current_difficulty = word_data[2] if len(word_data) > 2 else "Medium"
        self.current_group = word_data[3] if len(word_data) > 3 else ""
        self.current_examples = word_data[4] if len(word_data) > 4 else ""

        # Configure dialog
        self.title("Edit Word")
        self.geometry("750x700")  # Larger to fit examples
        self.resizable(False, False)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Create UI
        self._create_widgets()

        # Center dialog
        self._center_dialog()

        # Set focus
        self.difficulty_var.set(self.current_difficulty)

        # Wait for dialog to close
        self.wait_window()

    def _create_widgets(self) -> None:
        """Create all dialog widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Edit Word Properties",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Word information section
        self._create_word_info_section(main_frame)

        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(
            fill="x", pady=20
        )

        # Edit section
        self._create_edit_section(main_frame)

        # Buttons
        self._create_button_section(main_frame)

    def _create_word_info_section(self, parent: ttk.Frame) -> None:
        """Create section showing word information."""
        info_frame = ttk.LabelFrame(
            parent,
            text="Word Information",
            padding="10"
        )
        info_frame.pack(fill="x", pady=(0, 10))

        # English word
        english_frame = ttk.Frame(info_frame)
        english_frame.pack(fill="x", pady=5)

        ttk.Label(
            english_frame,
            text="English:",
            font=("Segoe UI", 10, "bold"),
            width=12,
            anchor="w"
        ).pack(side="left")

        ttk.Label(
            english_frame,
            text=self.english,
            font=("Segoe UI", 10)
        ).pack(side="left")

        # Hebrew word
        hebrew_frame = ttk.Frame(info_frame)
        hebrew_frame.pack(fill="x", pady=5)

        ttk.Label(
            hebrew_frame,
            text="Hebrew:",
            font=("Segoe UI", 10, "bold"),
            width=12,
            anchor="w"
        ).pack(side="left")

        ttk.Label(
            hebrew_frame,
            text=self.hebrew,
            font=("Segoe UI", 10)
        ).pack(side="left")

    def _create_edit_section(self, parent: ttk.Frame) -> None:
        """Create section for editing properties."""
        edit_frame = ttk.LabelFrame(
            parent,
            text="Edit Properties",
            padding="10"
        )
        edit_frame.pack(fill="both", expand=True)

        # Difficulty section
        self._create_difficulty_selector(edit_frame)

        # Group section
        self._create_group_selector(edit_frame)

        # Examples section
        self._create_examples_editor(edit_frame)

    def _create_difficulty_selector(self, parent: ttk.Frame) -> None:
        """Create difficulty selection section."""
        difficulty_container = ttk.Frame(parent)
        difficulty_container.pack(fill="x", pady=(0, 15))

        # Label
        ttk.Label(
            difficulty_container,
            text="Difficulty:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 8))

        # Radio buttons
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)

        for difficulty in self.DIFFICULTY_OPTIONS:
            rb = ttk.Radiobutton(
                difficulty_container,
                text=difficulty,
                value=difficulty,
                variable=self.difficulty_var
            )
            rb.pack(anchor="w", pady=2)

    def _create_group_selector(self, parent: ttk.Frame) -> None:
        """Create group selection/input section."""
        group_container = ttk.Frame(parent)
        group_container.pack(fill="x", pady=(0, 10))

        # Label
        label_frame = ttk.Frame(group_container)
        label_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(
            label_frame,
            text="Group:",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        ttk.Label(
            label_frame,
            text="(Select existing or type new)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).pack(side="left", padx=(5, 0))

        # Combobox (allows both selection and typing)
        self.group_var = tk.StringVar(value=self.current_group)
        self.group_combobox = ttk.Combobox(
            group_container,
            textvariable=self.group_var,
            values=self.available_groups,
            font=("Segoe UI", 10)
        )
        self.group_combobox.pack(fill="x")

        # Add placeholder if empty
        if not self.current_group:
            self.group_combobox.insert(0, "Enter or select group...")
            self.group_combobox.configure(foreground="gray")
            self.group_combobox.bind("<FocusIn>", self._clear_group_placeholder)
            self.group_combobox.bind("<FocusOut>", self._restore_group_placeholder)

    def _clear_group_placeholder(self, event: tk.Event) -> None:
        """Clear group placeholder on focus."""
        if self.group_combobox.get() == "Enter or select group...":
            self.group_combobox.delete(0, tk.END)
            self.group_combobox.configure(foreground="black")

    def _restore_group_placeholder(self, event: tk.Event) -> None:
        """Restore group placeholder if empty."""
        if not self.group_combobox.get():
            self.group_combobox.insert(0, "Enter or select group...")
            self.group_combobox.configure(foreground="gray")

    def _create_examples_editor(self, parent: ttk.Frame) -> None:
        """Create examples editor section."""
        examples_container = ttk.Frame(parent)
        examples_container.pack(fill="both", expand=True, pady=(15, 0))

        # Label
        label_frame = ttk.Frame(examples_container)
        label_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(
            label_frame,
            text="Examples:",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        ttk.Label(
            label_frame,
            text="(Enter example sentences using this word)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).pack(side="left", padx=(5, 0))

        # Text widget with scrollbar
        text_frame = ttk.Frame(examples_container)
        text_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget
        self.examples_text = tk.Text(
            text_frame,
            height=8,
            width=50,
            font=("Segoe UI", 10),
            wrap="word",
            yscrollcommand=scrollbar.set
        )
        self.examples_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.examples_text.yview)

        # Insert current examples
        if self.current_examples:
            self.examples_text.insert("1.0", self.current_examples)
        else:
            # Placeholder
            self.examples_text.insert("1.0", "Enter example sentences here...")
            self.examples_text.configure(foreground="gray")
            self.examples_text.bind("<FocusIn>", self._clear_examples_placeholder)
            self.examples_text.bind("<FocusOut>", self._restore_examples_placeholder)

    def _clear_examples_placeholder(self, event: tk.Event) -> None:
        """Clear examples placeholder on focus."""
        if self.examples_text.get("1.0", "end-1c") == "Enter example sentences here...":
            self.examples_text.delete("1.0", "end")
            self.examples_text.configure(foreground="black")

    def _restore_examples_placeholder(self, event: tk.Event) -> None:
        """Restore examples placeholder if empty."""
        if not self.examples_text.get("1.0", "end-1c").strip():
            self.examples_text.delete("1.0", "end")
            self.examples_text.insert("1.0", "Enter example sentences here...")
            self.examples_text.configure(foreground="gray")

    def _create_button_section(self, parent: ttk.Frame) -> None:
        """Create button section."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(20, 0))

        # Left side - Generate button
        generate_btn = ttk.Button(
            button_frame,
            text="🤖 Generate Examples",
            command=self._generate_examples,
            width=18
        )
        generate_btn.pack(side="left")

        # Right side - action buttons
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=12
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save Changes",
            command=self._on_save,
            width=12
        )
        save_btn.pack(side="right")

        sound_btn = ttk.Button(
            button_frame,
            text="Play Sound",
            command=self._sound,
            width=12
        )
        sound_btn.pack(side="right", padx=(0, 10))

        # Bind Enter key to save
        #self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())
        # self.bind(lambda e: self._sound())

    def _center_dialog(self) -> None:
        """Center the dialog on parent window."""
        self.update_idletasks()

        # Get parent position
        parent = self.master
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Get dialog size
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        # Calculate position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.geometry(f"+{x}+{y}")

    def _on_save(self) -> None:
        """Handle save button click."""
        # Get values
        difficulty = self.difficulty_var.get()
        group = self.group_var.get().strip()

        # Get examples
        examples = self.examples_text.get("1.0", "end-1c").strip()

        # Check if examples is placeholder
        if examples == "Enter example sentences here...":
            examples = ""

        # Check if group is placeholder
        if group == "Enter or select group...":
            group = ""

        # Validate
        if not difficulty:
            difficulty = "Medium"

        # Set result (difficulty, group, examples)
        self.result = (difficulty, group, examples)

        # Close dialog
        self.destroy()

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        self.result = None
        self.destroy()

    def _sound(self) -> None:
        play_sound(self.english)

    def _generate_examples(self) -> None:
        """Generate AI examples for the word."""
        try:
            # Try to import the example generator
            try:
                from Utils.ExampleGenerator import scrape_dictionary_com_examples

                # Show loading indicator
                current_text = self.examples_text.get("1.0", "end-1c")
                self.examples_text.delete("1.0", "end")
                self.examples_text.insert("1.0", "🤖 Generating examples... Please wait...")
                self.examples_text.configure(foreground="gray")
                self.update()

                # Generate examples
                examples = scrape_dictionary_com_examples(self.english)

                # Insert generated examples
                self.examples_text.delete("1.0", "end")

                if examples and not examples.startswith("Error"):
                    self.examples_text.insert("1.0", examples)
                    self.examples_text.configure(foreground="black")
                else:
                    # Show error and restore old text
                    self.examples_text.insert("1.0", current_text if current_text.strip() else "")
                    self.examples_text.configure(foreground="black")

                    from tkinter import messagebox
                    messagebox.showwarning(
                        "Generation Failed",
                        f"Could not generate examples:\n{examples}",
                        parent=self
                    )

            except ImportError:
                from tkinter import messagebox
                messagebox.showerror(
                    "Feature Not Available",
                    "ExampleGenerator not found.\n\n"
                    "Please add ExampleGenerator.py to your Utils folder.",
                    parent=self
                )

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Error",
                f"Failed to generate examples: {e}",
                parent=self
            )
        # self.destroy()


# ==================== Alternative: Simple Menu Dialog ====================

class WordActionDialog(tk.Toplevel):
    """
    Simple menu-based dialog for word actions.

    Provides quick access to:
    - Change difficulty
    - Change group
    - Delete word (optional)
    """

    def __init__(self, parent: tk.Widget, word_data: Tuple):
        """
        Initialize action dialog.

        Args:
            parent: Parent widget
            word_data: Tuple of (english, hebrew, difficulty, group)
        """
        super().__init__(parent)

        self.result: Optional[Tuple[str, any]] = None  # (action, value)
        self.word_data = word_data

        # Extract word info
        self.english = word_data[0] if len(word_data) > 0 else ""
        self.hebrew = word_data[1] if len(word_data) > 1 else ""

        # Configure dialog
        self.title("Word Actions")
        self.geometry("300x250")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Create UI
        self._create_widgets()
        self._center_dialog()

        self.wait_window()

    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text=f"Actions for: {self.english}",
            font=("Segoe UI", 11, "bold")
        )
        title.pack(pady=(0, 20))

        # Action buttons
        btn_width = 20

        change_diff_btn = ttk.Button(
            main_frame,
            text="Change Difficulty",
            command=self._change_difficulty,
            width=btn_width
        )
        change_diff_btn.pack(pady=5)

        change_group_btn = ttk.Button(
            main_frame,
            text="Change Group",
            command=self._change_group,
            width=btn_width
        )
        change_group_btn.pack(pady=5)

        ttk.Separator(main_frame, orient="horizontal").pack(
            fill="x", pady=15
        )

        cancel_btn = ttk.Button(
            main_frame,
            text="Cancel",
            command=self.destroy,
            width=btn_width
        )
        cancel_btn.pack(pady=5)

        # Bind Escape
        self.bind("<Escape>", lambda e: self.destroy())

    def _change_difficulty(self) -> None:
        """Open difficulty change dialog."""
        self.result = ("difficulty", None)
        self.destroy()

    def _change_group(self) -> None:
        """Open group change dialog."""
        self.result = ("group", None)
        self.destroy()

    def _center_dialog(self) -> None:
        """Center dialog on parent."""
        self.update_idletasks()
        parent = self.master
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ==================== Usage Example ====================

if __name__ == "__main__":
    """Test the dialogs."""

    root = tk.Tk()
    root.geometry("400x300")
    root.title("Dialog Test")


    def test_edit_dialog():
        word_data = ("hello", "שלום", "Medium", "Greetings")
        available_groups = ["Greetings", "Animals", "Food", "Colors", "Numbers"]

        dialog = WordEditDialog(root, word_data, available_groups)

        if dialog.result:
            difficulty, group = dialog.result
            print(f"New difficulty: {difficulty}")
            print(f"New group: {group}")
        else:
            print("Cancelled")


    def test_action_dialog():
        word_data = ("hello", "שלום", "Medium", "Greetings")
        dialog = WordActionDialog(root, word_data)

        if dialog.result:
            action, value = dialog.result
            print(f"Action selected: {action}")
        else:
            print("Cancelled")


    # Test buttons
    ttk.Button(
        root,
        text="Test Edit Dialog",
        command=test_edit_dialog
    ).pack(pady=20)

    ttk.Button(
        root,
        text="Test Action Dialog",
        command=test_action_dialog
    ).pack(pady=10)

    root.mainloop()
