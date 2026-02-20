import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Optional, Callable
import re

# ==================== Natural Sorting Function ====================

def natural_sort_key(text):
    def convert(part):
        """Convert to int if possible, otherwise lowercase string."""
        return int(part) if part.isdigit() else part.lower()

    # Split string into text and number parts
    parts = re.split(r'(\d+)', str(text) if text else "")

    # Convert number parts to integers
    return [convert(part) for part in parts]


# ==================== All Words Page ====================

class AllWordsPage(ttk.Frame):
    # Column configuration
    COLUMNS = ("English", "Hebrew", "Difficulty", "Group")
    COLUMN_CONFIG = {
        "English": {"width": 150, "anchor": "w"},
        "Hebrew": {"width": 350, "anchor": "w"},
        "Difficulty": {"width": 100, "anchor": "center"},
        "Group": {"width": 150, "anchor": "w"}
    }

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)

        # Data storage
        self.all_words_cache: List[Tuple] = []
        self._filtered_words: List[Tuple] = []
        self._sort_reverse: bool = False
        self._last_sort_column: Optional[str] = 'English'

        # Search state
        self.search_placeholder: str = "Search..."
        self._search_active: bool = False

        # Configure layout
        self._setup_grid()

        # Create UI components
        self._create_title()
        self._create_search_bar()
        self._create_statistics()
        self._create_table()
        self._create_footer()
        self._create_bottom_bar()

        # Bind events
        self._bind_events()

    def _setup_grid(self) -> None:
        """Configure grid weights for responsive layout."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)  # Table expands

    def _create_title(self) -> None:
        """Create and place the page title."""
        title = ttk.Label(
            self,
            text="All Words",
            font=("Segoe UI", 16, "bold")
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 10))

    def _create_search_bar(self) -> None:
        """Create search bar with placeholder functionality."""
        top_bar = ttk.Frame(self)
        top_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        top_bar.columnconfigure(0, weight=1)

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            top_bar,
            textvariable=self.search_var,
            font=("Segoe UI", 11)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Set initial placeholder
        self._set_search_placeholder()

    def _create_table(self) -> None:
        """Create the word table with scrollbar and sorting."""
        table_frame = ttk.Frame(self)
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Create treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=self.COLUMNS,
            show="headings",
            selectmode="browse"
        )

        # Configure columns with sorting
        for col in self.COLUMNS:
            self.tree.heading(
                col,
                text=col,
                anchor="w",
                command=lambda c=col: self._sort_by_column(c)
            )
            config = self.COLUMN_CONFIG[col]
            self.tree.column(col, width=config["width"], anchor=config["anchor"])

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Place treeview
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configure row tags for alternating colors
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="white")

    def _create_statistics(self) -> None:
        """Create statistics section showing word counts by difficulty."""
        stats_frame = ttk.Frame(self)
        stats_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Title
        title = ttk.Label(
            stats_frame,
            text="📊 Statistics:",
            font=("Segoe UI", 10, "bold")
        )
        title.pack(side="left", padx=(0, 15))

        # Difficulty count labels
        self.stat_new = ttk.Label(
            stats_frame,
            text="New: 0",
            font=("Segoe UI", 9),
            foreground="#757575"
        )
        self.stat_new.pack(side="left", padx=(0, 15))

        self.stat_easy = ttk.Label(
            stats_frame,
            text="Easy: 0",
            font=("Segoe UI", 9),
            foreground="#43a047"
        )
        self.stat_easy.pack(side="left", padx=(0, 15))

        self.stat_medium = ttk.Label(
            stats_frame,
            text="Medium: 0",
            font=("Segoe UI", 9),
            foreground="#fb8c00"
        )
        self.stat_medium.pack(side="left", padx=(0, 15))

        self.stat_hard = ttk.Label(
            stats_frame,
            text="Hard: 0",
            font=("Segoe UI", 9),
            foreground="#e53935"
        )
        self.stat_hard.pack(side="left")

    def _update_statistics(self) -> None:
        """Update statistics labels with word counts by difficulty."""
        counts = {
            "NEW_WORD": 0,
            "EASY": 0,
            "MEDIUM": 0,
            "HARD": 0
        }

        for word in self.all_words_cache:
            if len(word) >= 3:
                difficulty = str(word[2]).upper()
                if difficulty in counts:
                    counts[difficulty] += 1

        # Update labels
        self.stat_new.config(text=f"New: {counts['NEW_WORD']}")
        self.stat_easy.config(text=f"Easy: {counts['EASY']}")
        self.stat_medium.config(text=f"Medium: {counts['MEDIUM']}")
        self.stat_hard.config(text=f"Hard: {counts['HARD']}")

    def _create_footer(self) -> None:
        """Create footer with instructions."""
        self.footer_label = ttk.Label(
            self,
            text="Double-click to change difficulty • Click headers to sort",
            foreground="gray",
            font=("Segoe UI", 9)
        )
        self.footer_label.grid(row=4, column=0, sticky="w", pady=(8, 0))

    def _create_bottom_bar(self) -> None:
        """Create bottom bar with navigation and word count."""
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=5, column=0, sticky="ew", pady=(10, 0))

        # Home button
        self.add_word_btn = ttk.Button(
            bottom_bar,
            text="← Home Page"
        )
        self.add_word_btn.pack(side="left")

        # Word count label
        self.count_label = ttk.Label(
            bottom_bar,
            text="",
            foreground="gray",
            font=("Segoe UI", 9)
        )
        self.count_label.pack(side="left", padx=(20, 0))

    def _bind_events(self) -> None:
        """Bind all event handlers."""
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.search_entry.bind("<FocusIn>", self._clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_search_placeholder)

    # ==================== Placeholder Management ====================

    def _set_search_placeholder(self) -> None:
        """Set placeholder text in search entry."""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.configure(foreground="gray")
        self._search_active = False

    def _clear_search_placeholder(self, event: tk.Event) -> None:
        """Clear placeholder when focused."""
        if not self._search_active and self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground="black")
            self._search_active = True

    def _restore_search_placeholder(self, event: tk.Event) -> None:
        """Restore placeholder if empty."""
        if not self.search_entry.get():
            self._set_search_placeholder()

    # ==================== Data Display ====================

    def show_words(self, word_list: List[Tuple]) -> None:
        """Display words in the table."""
        self.all_words_cache = list(word_list)
        self._filtered_words = self.all_words_cache.copy()
        self._populate_tree(self._filtered_words)
        self._update_statistics()
        self._update_word_count()

    def _populate_tree(self, words: List[Tuple]) -> None:
        """Populate treeview with word data."""
        self.clear_treeview()

        for idx, word_tuple in enumerate(words):
            if len(word_tuple) >= 4:
                eng, heb, diff, group = word_tuple[:4]
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(eng, heb, diff, group), tags=(tag,))

    def clear_treeview(self) -> None:
        """Remove all items from the treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _update_word_count(self) -> None:
        """Update the word count display label."""
        total = len(self.all_words_cache)
        displayed = len(self._filtered_words)

        if displayed == total:
            self.count_label.config(text=f"Total: {total} word{'s' if total != 1 else ''}")
        else:
            self.count_label.config(text=f"Showing {displayed} of {total} words")

    # ==================== Search ====================

    def on_search(self, event: Optional[tk.Event] = None) -> None:
        """Filter words based on search query."""
        if not self._search_active:
            return

        query = self.search_var.get().strip().lower()

        if not query:
            self._filtered_words = self.all_words_cache.copy()
        else:
            self._filtered_words = [
                word for word in self.all_words_cache
                if self._matches_search(word, query)
            ]

        self._populate_tree(self._filtered_words)
        self._update_word_count()

    def _matches_search(self, word: Tuple, query: str) -> bool:
        """Check if word matches search query."""
        if len(word) < 4:
            return False

        english, hebrew, difficulty, group = word[:4]
        searchable_fields = [english, hebrew, group]

        return any(
            query in str(field).lower()
            for field in searchable_fields
            if field is not None
        )

    # ==================== Sorting (WITH NATURAL SORT!) ====================

    def _sort_by_column(self, column: str) -> None:
        # Determine column index
        try:
            col_index = self.COLUMNS.index(column)
        except ValueError:
            return

        # Toggle sort direction if same column
        if self._last_sort_column == column:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_reverse = False
            self._last_sort_column = column

        # Sort the filtered words
        try:
            if column == "Difficulty":
                # Numeric sort for difficulty
                self._filtered_words.sort(
                    key=lambda x: self._get_difficulty_value(x[col_index]),
                    reverse=self._sort_reverse
                )
            elif column == "Group":
                # 🌟 NATURAL SORT FOR GROUPS! 🌟
                # This fixes the 1, 10, 19, 2 problem
                self._filtered_words.sort(
                    key=lambda x: natural_sort_key(x[col_index]),
                    reverse=self._sort_reverse
                )
            else:
                # Alphabetical sort for other columns
                self._filtered_words.sort(
                    key=lambda x: str(x[col_index]).lower() if x[col_index] else "",
                    reverse=self._sort_reverse
                )
        except (IndexError, TypeError) as e:
            print(f"Sort error: {e}")
            return

        # Refresh display
        self._populate_tree(self._filtered_words)

        # Update header to show sort direction
        self._update_sort_indicator(column)

    def _get_difficulty_value(self, difficulty: any) -> int:
        """Convert difficulty to numeric value for sorting."""
        if difficulty is None:
            return 0

        try:
            return int(difficulty)
        except (ValueError, TypeError):
            pass

        difficulty_map = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }

        return difficulty_map.get(str(difficulty).lower(), 0)

    def _update_sort_indicator(self, column: str) -> None:
        """Update column header to show sort direction."""
        for col in self.COLUMNS:
            if col == column:
                indicator = " ↓" if self._sort_reverse else " ↑"
                self.tree.heading(col, text=f"{col}{indicator}")
            else:
                self.tree.heading(col, text=col)

    # ==================== Public API ====================

    def get_selected_word(self) -> Optional[Tuple]:
        """Get the currently selected word data."""
        selection = self.tree.selection()
        if not selection:
            return None

        values = self.tree.item(selection[0], "values")
        return values if values else None

    def refresh_display(self) -> None:
        """Refresh the current display."""
        self._populate_tree(self._filtered_words)
        self._update_word_count()
