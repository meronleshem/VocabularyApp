from typing import Optional, Tuple, List
import tkinter as tk
from tkinter import messagebox

try:
    from View.View import ViewManager
    from Database.DatabaseManager import DatabaseManager
    from Controllers.WordEditDialog import WordEditDialog  # New dialog
    from Utils.DiffucltyEnum import Difficulty
except ImportError as e:
    print(f"Import warning: {e}")
    # Define fallback types for development
    ViewManager = DatabaseManager = WordEditDialog = Difficulty = None


class AllWordsController:
    def __init__(self, model: 'DatabaseManager', view: 'ViewManager') -> None:
        self.model = model
        self.view = view
        self.page = view.pages.get("all_words_page")

        if self.page is None:
            raise ValueError("All Words page not found in view")

        # Bind events and initialize
        self._bind_events()

    def _bind_events(self) -> None:
        """Bind UI events to controller methods."""
        # Home button
        if hasattr(self.page, 'add_word_btn'):
            self.page.add_word_btn.config(command=self.switch_to_home)

        if hasattr(self.page, 'delete_word_btn'):
            self.page.delete_word_btn.config(command=self.delete_selected_word)

        # Double-click on table row
        if hasattr(self.page, 'tree'):
            self.page.tree.bind("<Double-Button-1>", self.on_word_double_click)

    # ==================== Data Loading ====================

    def show_words(self) -> None:
        """Load and display all words from the database."""
        try:
            words_list = self.model.get_full_data()

            if words_list:
                self.page.show_words(words_list)
            else:
                self.page.show_words([])
                self._show_info("No words found", "The vocabulary list is empty.")

        except AttributeError as e:
            self._show_error("Data Error", f"Failed to load words: {e}")
        except Exception as e:
            self._show_error("Unexpected Error", f"An error occurred: {e}")

    def refresh_words(self, preserve_view: bool = True) -> None:
        if preserve_view:
            # Save current state (with None checks)
            last_sort = getattr(self.page, '_last_sort_column', None)
            sort_reverse = getattr(self.page, '_sort_reverse', False)

            # Get currently selected item
            selection = self.page.tree.selection()
            selected_values = None
            if selection:
                try:
                    selected_values = self.page.tree.item(selection[0], 'values')
                except:
                    pass

            # Reload data
            self.show_words()

            # Restore sort order ONLY if there was one
            if last_sort is not None:
                try:
                    self.page._sort_by_column(last_sort)
                    # Check if we need to flip direction
                    current_reverse = getattr(self.page, '_sort_reverse', False)
                    if sort_reverse != current_reverse:
                        # Sort again to flip direction
                        self.page._sort_by_column(last_sort)
                except Exception as e:
                    print(f"Could not restore sort: {e}")

            # Restore selection
            if selected_values:
                try:
                    for item in self.page.tree.get_children():
                        if self.page.tree.item(item, 'values') == selected_values:
                            self.page.tree.selection_set(item)
                            self.page.tree.see(item)
                            break
                except Exception as e:
                    print(f"Could not restore selection: {e}")
        else:
            self.show_words()

    # ==================== Event Handlers ====================

    def on_word_double_click(self, event: tk.Event) -> None:
        # Get selected word
        word_data = self._get_selected_word()
        if not word_data:
            return

        # Get full word details from database
        try:
            english_word = word_data[0]
            details = self.model.get_word_details(english_word)

            if not details:
                self._show_error("Error", f"Could not find details for '{english_word}'")
                return

            # Show edit dialog
            self._show_edit_dialog(details, word_data)

        except Exception as e:
            self._show_error("Error", f"Failed to process word: {e}")

    def _show_edit_dialog(self, word_details: Tuple, display_data: Tuple) -> None:
        if not word_details or len(word_details) < 4:
            self._show_error("Error", "Invalid word details")
            return

        try:
            # Get available groups for dropdown
            available_groups = self._get_available_groups()

            word_data_with_examples = (
                word_details[1],  # english
                word_details[2],  # hebrew
                word_details[4],  # difficulty
                word_details[5],  # group
                word_details[3]  # examples
            )

            # Show dialog
            dialog = WordEditDialog(self.page, word_data_with_examples, available_groups)

            if dialog.result:
                new_difficulty, new_group, new_examples = dialog.result  # Now 3 values!

                # Update database
                changes_made = self._update_word_properties(word_details, new_difficulty, new_group, new_examples)

                if changes_made:
                    # Refresh display
                    self.refresh_words()

                    # Show success message
                    self._show_info(
                        "Success",
                        f"Word updated successfully!\nDifficulty: {new_difficulty}\nGroup: {new_group or '(none)'}"
                    )

        except AttributeError:
            self._show_error(
                "Error",
                "WordEditDialog not available. Check imports."
            )
        except Exception as e:
            self._show_error("Error", f"Failed to update word: {e}")

    def _update_word_properties(self, word_details: Tuple,
                                new_difficulty: str,
                                new_group: str,
                                new_examples=None) -> bool:
        changes_made = False
        hebrew_word = word_details[1]  # Primary key

        # Convert difficulty to enum
        difficulty_enum = self._convert_difficulty_to_enum(new_difficulty)

        if difficulty_enum:
            try:
                # Update difficulty
                self.model.update_difficulty(hebrew_word, difficulty_enum)
                changes_made = True
            except Exception as e:
                self._show_error("Error", f"Failed to update difficulty: {e}")
                return False

        # Update group if method exists
        if hasattr(self.model, 'update_group'):
            try:
                self.model.update_group(hebrew_word, new_group)
                changes_made = True
            except Exception as e:
                self._show_error("Error", f"Failed to update group: {e}")
                return False
        elif new_group != word_details[3]:  # If group changed but no update method
            self._show_warning(
                "Feature Not Available",
                "Group updating is not yet implemented in the database."
            )

        if new_examples is not None:
            self.model.cursor.execute(
                "UPDATE vocabulary SET examples = ? WHERE engWord = ?",
                (new_examples, word_details[1])
            )
            self.model.connection.commit()

        return changes_made

    def delete_selected_word(self) -> None:
        # Get selected word
        selected = self.page.get_selected_word()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a word to delete.",
                parent=self.page
            )
            return

        english_word = selected[0]
        hebrew_word = selected[1] if len(selected) > 1 else ""

        # Confirmation dialog
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this word?\n\n"
            f"English: {english_word}\n"
            f"Hebrew: {hebrew_word}\n\n"
            f"This action cannot be undone!",
            parent=self.page,
            icon='warning'
        )

        if not result:
            return  # User cancelled

        # Delete from database
        try:
            success = self.model.delete_word(english_word)

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Word '{english_word}' has been deleted.",
                    parent=self.page
                )
                # Refresh the display
                self.show_words()
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to delete word '{english_word}'.",
                    parent=self.page
                )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred:\n{str(e)}",
                parent=self.page
            )

    def _get_available_groups(self) -> List[str]:
        try:
            # Check if method exists
            if hasattr(self.model, 'get_all_groups'):
                groups = self.model.get_all_groups()
                return sorted(set(groups)) if groups else []

            # Fallback: extract groups from full data
            words = self.model.get_full_data()
            groups = set()

            for word in words:
                if len(word) >= 4 and word[3]:  # Has group
                    groups.add(word[3])

            return sorted(groups)

        except Exception as e:
            print(f"Error getting groups: {e}")
            return []

    def _convert_difficulty_to_enum(self, difficulty_str: str) -> Optional[str]:
        if not Difficulty:
            # Fallback if enum not available
            return difficulty_str.upper()

        difficulty_map = {
            "Easy": Difficulty.EASY.name,
            "Medium": Difficulty.MEDIUM.name,
            "Hard": Difficulty.HARD.name
        }

        return difficulty_map.get(difficulty_str)

    # ==================== Navigation ====================

    def switch_to_home(self) -> None:
        """Navigate to the home/add word page."""
        try:
            if "add_word_page" in self.view.pages:
                self.view.show_page(self.view.pages["add_word_page"])
            else:
                self._show_error("Error", "Home page not available")
        except Exception as e:
            self._show_error("Navigation Error", f"Failed to switch page: {e}")

    # ==================== Helper Methods ====================

    def _get_selected_word(self) -> Optional[Tuple]:
        try:
            selection = self.page.tree.selection()
            if not selection:
                return None

            values = self.page.tree.item(selection[0], 'values')
            return values if values else None

        except (AttributeError, tk.TclError) as e:
            print(f"Error getting selection: {e}")
            return None

    def _show_info(self, title: str, message: str) -> None:
        messagebox.showinfo(title, message, parent=self.page)

    def _show_warning(self, title: str, message: str) -> None:
        messagebox.showwarning(title, message, parent=self.page)

    def _show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message, parent=self.page)

    # ==================== Public API ====================

    def initialize(self) -> None:
        """Initialize the controller and load initial data."""
        self.show_words()

    def cleanup(self) -> None:
        """Cleanup resources when controller is destroyed."""
        # Add any cleanup logic here
        pass


# ==================== Enhanced Controller (Optional) ====================

class EnhancedAllWordsController(AllWordsController):
    def __init__(self, model: 'DatabaseManager', view: 'ViewManager') -> None:
        super().__init__(model, view)
        self._setup_enhanced_features()

    def _setup_enhanced_features(self) -> None:
        """Setup additional features."""
        # Could add context menu, bulk operations, etc.
        pass

    def create_new_group(self, group_name: str) -> bool:
        try:
            if hasattr(self.model, 'create_group'):
                self.model.create_group(group_name)
                return True
            return False
        except Exception as e:
            self._show_error("Error", f"Failed to create group: {e}")
            return False

    def rename_group(self, old_name: str, new_name: str) -> bool:
        try:
            if hasattr(self.model, 'rename_group'):
                self.model.rename_group(old_name, new_name)
                self.refresh_words()
                return True
            return False
        except Exception as e:
            self._show_error("Error", f"Failed to rename group: {e}")
            return False

    def delete_group(self, group_name: str, reassign_to: Optional[str] = None) -> bool:
        try:
            if hasattr(self.model, 'delete_group'):
                self.model.delete_group(group_name, reassign_to)
                self.refresh_words()
                return True
            return False
        except Exception as e:
            self._show_error("Error", f"Failed to delete group: {e}")
            return False

    def export_words(self, filename: str) -> bool:
        try:
            words = self.model.get_full_data()
            # Implement export logic
            # Could support CSV, JSON, etc.
            return True
        except Exception as e:
            self._show_error("Export Error", f"Failed to export: {e}")
            return False

    def get_statistics(self) -> dict:
        words = self.model.get_full_data()

        return {
            "total": len(words),
            "by_difficulty": self._count_by_difficulty(words),
            "by_group": self._count_by_group(words)
        }

    def _count_by_difficulty(self, words: list) -> dict:
        """Count words by difficulty level."""
        counts = {}
        for word in words:
            if len(word) >= 3:
                difficulty = word[2]
                counts[difficulty] = counts.get(difficulty, 0) + 1
        return counts

    def _count_by_group(self, words: list) -> dict:
        """Count words by group."""
        counts = {}
        for word in words:
            if len(word) >= 4:
                group = word[3] or "(No Group)"
                counts[group] = counts.get(group, 0) + 1
        return counts
