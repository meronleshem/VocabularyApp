"""
View Manager - Smart window sizing

Features:
- Automatically resizes window based on page
- Smooth transitions
- Optimal size for each page
"""
import tkinter as tk
from ttkbootstrap import Style
from View.AddWordPage import AddWordPage
from View.AllWordsPage import AllWordsPage
from View.QuizPage import QuizPage
from View.FillBlankQuizPage import FillBlankQuizPage


class ViewManager(tk.Tk):
    """
    Main application window with smart sizing.

    Automatically adjusts window size based on the page being displayed.
    """

    # Page-specific sizes
    PAGE_SIZES = {
        "add_word_page": ("850x600", 800, 550),  # (geometry, min_width, min_height)
        "all_words_page": ("1000x700", 900, 650),
        "quiz_page": ("1100x850", 950, 700),
        "fill_blank_quiz_page": ("1100x750", 950, 700)
    }

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Vocabulary App")
        self.geometry("850x600")  # Start with home page size
        self.minsize(800, 550)

        # Apply theme
        self.style = Style("sandstone")

        # Create container
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Configure main window grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create pages
        self.pages = {
            "add_word_page": AddWordPage(self.container),
            "all_words_page": AllWordsPage(self.container),
            "quiz_page": QuizPage(self.container),
            "fill_blank_quiz_page": FillBlankQuizPage(self.container)
        }

        # Track current page
        self.curr_page = None
        self.curr_page_name = None

        # Show initial page
        self.show_page_by_name("add_word_page")

    def show_page(self, page):
        """
        Display a page (with name lookup for resizing).

        Args:
            page: Page frame to display
        """
        # Find page name
        page_name = None
        for name, pg in self.pages.items():
            if pg == page:
                page_name = name
                break

        if page_name:
            self.show_page_by_name(page_name)
        else:
            # Fallback - show without resizing
            self.curr_page = page
            page.grid(row=0, column=0, padx=50, pady=30, sticky="nsew")
            page.tkraise()

    def show_page_by_name(self, page_name: str):
        """
        Display a page by name and resize window accordingly.

        Args:
            page_name: Name of the page to display
        """
        if page_name not in self.pages:
            print(f"Warning: Page '{page_name}' not found")
            return

        page = self.pages[page_name]

        # Resize window if size info available
        if page_name in self.PAGE_SIZES:
            geometry, min_w, min_h = self.PAGE_SIZES[page_name]

            # Only resize if actually changing pages (not on initial load)
            if self.curr_page_name != page_name:
                self.geometry(geometry)
                self.minsize(min_w, min_h)

        # Update current page
        self.curr_page = page
        self.curr_page_name = page_name

        # Display page
        page.grid(row=0, column=0, padx=50, pady=30, sticky="nsew")
        page.tkraise()

