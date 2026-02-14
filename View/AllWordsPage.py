"""
All Words Page - Display and manage vocabulary words

This module provides a GUI page for viewing, searching, and managing
vocabulary words in a table format.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Optional, Callable


class AllWordsPage(ttk.Frame):
    """
    A page displaying vocabulary words in a searchable, sortable table.

    Features:
    - Search functionality with placeholder text
    - Sortable columns (click headers)
    - Double-click to change difficulty
    - Responsive layout with alternating row colors
    - Word count display

    Attributes:
        all_words_cache: Cached list of all words
        search_var: StringVar for search input
        tree: Treeview widget displaying words
        add_word_btn: Button to return to home page
    """

    # Column configuration
    COLUMNS = ("English", "Hebrew", "Difficulty", "Group")
    COLUMN_CONFIG = {
        "English": {"width": 150, "anchor": "w"},
        "Hebrew": {"width": 350, "anchor": "w"},
        "Difficulty": {"width": 100, "anchor": "center"},
        "Group": {"width": 150, "anchor": "w"}
    }

    def __init__(self, parent: tk.Widget) -> None:
        """
        Initialize the All Words page.

        Args:
            parent: Parent widget/container
        """
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
        self._create_table()
        self._create_footer()
        self._create_bottom_bar()

        # Bind events
        self._bind_events()

    def _setup_grid(self) -> None:
        """Configure grid weights for responsive layout."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)  # Table expands

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
        table_frame.grid(row=2, column=0, sticky="nsew")
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

    def _create_footer(self) -> None:
        """Create footer with instructions."""
        self.footer_label = ttk.Label(
            self,
            text="Double-click to change difficulty • Click headers to sort",
            foreground="gray",
            font=("Segoe UI", 9)
        )
        self.footer_label.grid(row=3, column=0, sticky="w", pady=(8, 0))

    def _create_bottom_bar(self) -> None:
        """Create bottom bar with navigation and word count."""
        bottom_bar = ttk.Frame(self)
        bottom_bar.grid(row=4, column=0, sticky="ew", pady=(10, 0))

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
        # Double-click binding is handled in controller

    # ==================== Search Placeholder Management ====================

    def _set_search_placeholder(self) -> None:
        """Set the search placeholder text and styling."""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.configure(foreground="gray")
        self._search_active = False

    def _clear_search_placeholder(self, event: tk.Event) -> None:
        """
        Clear placeholder text when entry gains focus.

        Args:
            event: Focus event
        """
        if not self._search_active and self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground="black")
            self._search_active = True

    def _restore_search_placeholder(self, event: tk.Event) -> None:
        """
        Restore placeholder if entry is empty when losing focus.

        Args:
            event: Focus event
        """
        if not self.search_entry.get():
            self._set_search_placeholder()

    # ==================== Data Display Methods ====================

    def show_words(self, word_list: List[Tuple]) -> None:
        """
        Display words in the table.

        Args:
            word_list: List of tuples (english, hebrew, difficulty, group)
        """

        self.all_words_cache = list(word_list)
        self._filtered_words = self.all_words_cache.copy()
        #self.all_words_cache = word_list.copy()
        #self._filtered_words = word_list.copy()
        self._populate_tree(self._filtered_words)
        self._update_word_count()

    def _populate_tree(self, words: List[Tuple]) -> None:
        """
        Populate treeview with word data.

        Args:
            words: List of word tuples to display
        """
        self.clear_treeview()

        for idx, word_tuple in enumerate(words):
            # Validate tuple has correct number of elements
            if len(word_tuple) >= 4:
                eng, heb, diff, group = word_tuple[:4]
                # Alternate row colors
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

    # ==================== Search Functionality ====================

    def on_search(self, event: Optional[tk.Event] = None) -> None:
        """
        Filter words based on search query.

        Args:
            event: Key release event (optional)
        """
        # Skip if placeholder is showing
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
        """
        Check if a word matches the search query.

        Args:
            word: Word tuple (english, hebrew, difficulty, group)
            query: Search query string (lowercase)

        Returns:
            True if word matches query
        """
        if len(word) < 4:
            return False

        english, hebrew, difficulty, group = word[:4]

        # Search in all relevant fields
        searchable_fields = [english, hebrew, group]

        return any(
            query in str(field).lower()
            for field in searchable_fields
            if field is not None
        )

    # ==================== Sorting Functionality ====================

    def _sort_by_column(self, column: str) -> None:
        """
        Sort the table by the specified column.

        Args:
            column: Column name to sort by
        """
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
        """
        Convert difficulty to numeric value for sorting.

        Args:
            difficulty: Difficulty value (string or number)

        Returns:
            Numeric value for sorting
        """
        if difficulty is None:
            return 0

        # Try direct conversion to int
        try:
            return int(difficulty)
        except (ValueError, TypeError):
            pass

        # Map text difficulty to numbers
        difficulty_map = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }

        return difficulty_map.get(str(difficulty).lower(), 0)

    def _update_sort_indicator(self, column: str) -> None:
        """
        Update column header to show sort direction.

        Args:
            column: Column being sorted
        """
        # Update all headers
        for col in self.COLUMNS:
            if col == column:
                indicator = " ↓" if self._sort_reverse else " ↑"
                self.tree.heading(col, text=f"{col}{indicator}")
            else:
                self.tree.heading(col, text=col)

    # ==================== Event Handlers ====================

    def on_double_click(self, event: tk.Event) -> None:
        """
        Handle double-click event on table row.
        This method is kept for backward compatibility but should
        be bound in the controller.

        Args:
            event: Double-click event
        """
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item[0], "values")
        print(f"Double-clicked: {values}")

    # ==================== Public API Methods ====================

    def get_selected_word(self) -> Optional[Tuple]:
        """
        Get the currently selected word data.

        Returns:
            Tuple of (english, hebrew, difficulty, group) or None
        """
        selection = self.tree.selection()
        if not selection:
            return None

        values = self.tree.item(selection[0], "values")
        return values if values else None

    def refresh_display(self) -> None:
        """Refresh the current display (useful after data updates)."""
        self._populate_tree(self._filtered_words)
        self._update_word_count()

