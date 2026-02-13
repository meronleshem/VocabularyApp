# import tkinter as tk
# from ttkbootstrap import Style
# from View.AddWordPage import AddWordPage
# from View.AllWordsPage import AllWordsPage
# from View.QuizPage import QuizPage
#
#
# class ViewManager(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Vocabulary App")
#         self.geometry("850x500")
#
#         self.style = Style("sandstone")
#
#         self.container = tk.Frame(self)
#         self.container.grid(row=0, column=0, sticky="nsew")
#         self.container.grid_rowconfigure(0, weight=1)
#         self.container.grid_columnconfigure(0, weight=1)
#
#         self.pages = {
#             "add_word_page": AddWordPage(self.container),
#             "all_words_page": AllWordsPage(self.container),
#             "quiz_page": QuizPage(self.container)
#         }
#
#         self.curr_page = None
#         self.show_page(self.pages["add_word_page"])
#
#     def show_page(self, page):
#         self.curr_page = page
#         self.curr_page.grid(row=0, column=0, padx=50, pady=30, sticky="nsew")
#         self.curr_page.tkraise()

"""
View Manager - Main window and page navigation

This module manages the main application window and handles
navigation between different pages.
"""
import tkinter as tk
from typing import Dict, Optional
from ttkbootstrap import Style

# Import page classes
try:
    from View.AddWordPage import AddWordPage
    from View.AllWordsPage import AllWordsPage
    from View.QuizPage import QuizPage
except ImportError:
    # Fallback for testing
    print("Warning: Page imports failed. Make sure View package is in PYTHONPATH")
    AddWordPage = AllWordsPage = QuizPage = None


class ViewManager(tk.Tk):
    """
    Main application window managing multiple pages.

    Handles:
    - Window initialization and configuration
    - Page creation and management
    - Navigation between pages
    - Theme/style management

    Attributes:
        container: Main container frame for pages
        pages: Dictionary mapping page names to page instances
        curr_page: Currently displayed page
        style: ttkbootstrap style manager
    """

    # Window configuration
    DEFAULT_WIDTH = 850
    DEFAULT_HEIGHT = 500
    MIN_WIDTH = 700
    MIN_HEIGHT = 400

    # Page names
    PAGE_ADD_WORD = "add_word_page"
    PAGE_ALL_WORDS = "all_words_page"
    PAGE_QUIZ = "quiz_page"

    def __init__(self, title: str = "Vocabulary App", theme: str = "sandstone") -> None:
        """
        Initialize the main application window.

        Args:
            title: Window title
            theme: ttkbootstrap theme name
        """
        super().__init__()

        # Window setup
        self.title(title)
        self.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Apply theme
        try:
            self.style = Style(theme)
        except Exception as e:
            print(f"Warning: Failed to apply theme '{theme}': {e}")
            self.style = None

        # Initialize variables
        self.pages: Dict[str, tk.Frame] = {}
        self.curr_page: Optional[tk.Frame] = None

        # Setup UI
        self._create_container()
        self._create_pages()

        # Show initial page
        self._show_initial_page()

        # Configure window behavior
        self._configure_window()

    def _create_container(self) -> None:
        """Create the main container frame for pages."""
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        # Make container expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _create_pages(self) -> None:
        """Initialize all application pages."""
        # Only create pages if imports were successful
        if AddWordPage and AllWordsPage and QuizPage:
            try:
                self.pages = {
                    self.PAGE_ADD_WORD: AddWordPage(self.container),
                    self.PAGE_ALL_WORDS: AllWordsPage(self.container),
                    self.PAGE_QUIZ: QuizPage(self.container)
                }
            except Exception as e:
                print(f"Error creating pages: {e}")
                self.pages = {}
        else:
            print("Warning: Page classes not available")

    def _show_initial_page(self) -> None:
        """Display the initial page."""
        if self.PAGE_ADD_WORD in self.pages:
            self.show_page(self.pages[self.PAGE_ADD_WORD])
        elif self.pages:
            # Show first available page
            first_page = next(iter(self.pages.values()))
            self.show_page(first_page)

    def _configure_window(self) -> None:
        """Configure additional window properties."""
        # Center window on screen
        self.update_idletasks()
        self._center_window()

        # Set window icon if available
        try:
            # self.iconbitmap('path/to/icon.ico')  # Uncomment and set path
            pass
        except Exception:
            pass

    def _center_window(self) -> None:
        """Center the window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.DEFAULT_WIDTH) // 2
        y = (screen_height - self.DEFAULT_HEIGHT) // 2

        self.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}+{x}+{y}")

    # ==================== Page Navigation ====================

    def show_page(self, page: tk.Frame) -> None:
        """
        Display the specified page.

        Args:
            page: Page frame to display
        """
        if page is None:
            print("Warning: Attempted to show None page")
            return

        # Update current page reference
        self.curr_page = page

        # Configure and display page
        page.grid(row=0, column=0, padx=50, pady=30, sticky="nsew")
        page.tkraise()

    def show_page_by_name(self, page_name: str) -> bool:
        """
        Display a page by its name.

        Args:
            page_name: Name of the page to display

        Returns:
            True if page was shown successfully, False otherwise
        """
        if page_name in self.pages:
            self.show_page(self.pages[page_name])
            return True
        else:
            print(f"Warning: Page '{page_name}' not found")
            return False

    def get_page(self, page_name: str) -> Optional[tk.Frame]:
        """
        Get a page by its name.

        Args:
            page_name: Name of the page to retrieve

        Returns:
            Page frame or None if not found
        """
        return self.pages.get(page_name)

    # ==================== Convenience Methods ====================

    def show_add_word_page(self) -> None:
        """Show the Add Word page."""
        self.show_page_by_name(self.PAGE_ADD_WORD)

    def show_all_words_page(self) -> None:
        """Show the All Words page."""
        self.show_page_by_name(self.PAGE_ALL_WORDS)

    def show_quiz_page(self) -> None:
        """Show the Quiz page."""
        self.show_page_by_name(self.PAGE_QUIZ)

    # ==================== Window Management ====================

    def set_title(self, title: str) -> None:
        """
        Set the window title.

        Args:
            title: New window title
        """
        self.title(title)

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        current_state = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current_state)

    def quit_application(self) -> None:
        """Safely quit the application."""
        # Perform any cleanup here
        self.quit()
        self.destroy()


# def main() -> None:
#     """Run the application (for testing)."""
#     app = ViewManager()
#     app.mainloop()
#
#
# if __name__ == "__main__":
#     main()
