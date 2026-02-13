import sqlite3
from Utils.DiffucltyEnum import Difficulty
from Utils.Translator import translate_to_heb, get_word_examples
from Utils.FileHandler import read_words_from_file, extract_highlight_words_from_pdf


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect('Database\\vocabulary.db')
        self.cursor = self.connection.cursor()
        self.table_name = "vocabulary"

    def create_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vocabulary
                       (id INTEGER PRIMARY KEY,
                        engWord TEXT,
                        hebWord TEXT,
                        examples TEXT,
                        difficulty TEXT,
                        group_name TEXT)''')

        raw_data1 = (1, "remorse", translate_to_heb("remorse"), get_word_examples("remorse"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data2 = (2, "chore", translate_to_heb("chore"), get_word_examples("chore"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data3 = (3, "more", translate_to_heb("more"), get_word_examples("more"), Difficulty.EASY.name, "The_Silent_Patient_1")
        raw_data4 = (4, "vigour", translate_to_heb("vigour"), get_word_examples("vigour"), Difficulty.EASY.name, "The_Silent_Patient_1")

        self.cursor.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data1)
        self.cursor.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data2)
        self.cursor.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data3)
        self.cursor.execute("INSERT INTO vocabulary (id, engWord, hebWord, examples, difficulty, group_name)"
                         " VALUES (?, ?, ?, ?, ?, ?)", raw_data4)
        self.connection.commit()

    def print_db_data(self):
        data = self.cursor.execute(f"SELECT * FROM {self.table_name}")

        for item in data:
            print(item)

    def get_data(self):
        return self.cursor.execute(f"SELECT engWord, hebWord FROM {self.table_name}")

    def get_full_data(self):
        return self.cursor.execute(f"SELECT engWord, hebWord, difficulty, group_name FROM {self.table_name}")

    def add_word(self, eng_word, group_name="New_Words"):
        if self.is_word_exists(eng_word):
            print(f"{eng_word} is already exists. Abort adding")
            return

        heb_word = translate_to_heb(eng_word)
        if heb_word is None:
            print(f"{eng_word} is not a valid word. Abort adding")
            return

        num_of_words = self.get_table_size()
        word_id = num_of_words + 1
        examples = get_word_examples(eng_word)

        word_data = (word_id, eng_word.lower(), heb_word, examples, Difficulty.NEW_WORD.name, group_name)
        self.cursor.execute(f"INSERT INTO {self.table_name}"
                         f" (id, engWord, hebWord, examples, difficulty, group_name) VALUES (?, ?, ?, ?, ?, ?)", word_data)

        self.connection.commit()

        print(f"{eng_word} was added!")

    def add_from_file(self, filepath, group_name):
        words_to_add = read_words_from_file(filepath)
        for word in words_to_add:
            self.add_word(word, group_name)

    def update_difficulty(self, eng_word, difficulty):
        self.cursor.execute(f"UPDATE {self.table_name}"
                         f" SET difficulty = ? WHERE engWord = ?", (difficulty, eng_word))

        self.connection.commit()

    def delete_word(self, eng_word):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))

        self.connection.commit()

    def is_word_exists(self, eng_word):
        data = self.cursor.execute(f"SELECT engWord FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))
        res = data.fetchone()

        return res is not None

    def add_highlight_words_from_pdf(self, filepath):
        words_to_add = extract_highlight_words_from_pdf(filepath)
        for word, pack in words_to_add:
            group_name = f"The Blade Itself {pack}"
            self.add_word(word, group_name)

    def get_table_size(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return self.cursor.fetchone()[0]

    def get_word_details(self, eng_word):
        data = self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE engWord = ?", (eng_word.lower(),))

        for item in data:
            return item

    def get_words_by_groups(self, selected_groups):
        query = f"SELECT engWord, hebWord, difficulty, group_name FROM vocabulary WHERE group_name IN ({','.join('?' for _ in selected_groups)})"
        self.cursor.execute(query, selected_groups)
        return self.cursor.fetchall()

    def get_all_groups_names(self):
        self.cursor.execute("SELECT DISTINCT group_name FROM vocabulary")
        return self.cursor.fetchall()

    def close_db_connection(self):
        self.cursor.close()
        self.connection.close()

    """
    Database Manager Extensions for Group Management

    Add these methods to your DatabaseManager class to support group operations.
    This is a reference implementation - adapt to your existing database structure.
    """

    # ==================== Add to DatabaseManager class ====================

    def update_group(self, engWord: str, new_group: str) -> bool:
        """
        Update the group for a specific word.

        Args:
            engWord: Hebrew word (primary key)
            new_group: New group name

        Returns:
            True if successful

        Usage:
            db.update_group("שלום", "Greetings")
        """
        try:
            # Example SQL implementation
            # Adjust based on your table structure
            cursor = self.connection.cursor()

            query = """
                UPDATE vocabulary 
                SET group_name = ? 
                WHERE engWord = ?
            """

            cursor.execute(query, (new_group, engWord))
            self.connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error updating group: {e}")
            self.connection.rollback()
            return False

    def get_all_groups(self) -> list:
        """
        Get list of all unique groups.

        Returns:
            List of group names

        Usage:
            groups = db.get_all_groups()
            # Returns: ["Greetings", "Animals", "Food", ...]
        """
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT DISTINCT group_name 
                FROM vocabulary 
                WHERE group_name IS NOT NULL AND group_name != ''
                ORDER BY group_name
            """

            cursor.execute(query)
            results = cursor.fetchall()

            return [row[0] for row in results]

        except Exception as e:
            print(f"Error getting groups: {e}")
            return []

    def create_group(self, group_name: str) -> bool:
        """
        Create a new group (if your database has a separate groups table).

        Args:
            group_name: Name of the group to create

        Returns:
            True if successful

        Usage:
            db.create_group("New Category")
        """
        try:
            # If you have a separate groups table
            cursor = self.connection.cursor()

            query = """
                INSERT INTO groups (name) 
                VALUES (?)
            """

            cursor.execute(query, (group_name,))
            self.connection.commit()

            return True

        except Exception as e:
            print(f"Error creating group: {e}")
            self.connection.rollback()
            return False

    def rename_group(self, old_name: str, new_name: str) -> bool:
        """
        Rename a group (updates all words in that group).

        Args:
            old_name: Current group name
            new_name: New group name

        Returns:
            True if successful

        Usage:
            db.rename_group("Old Name", "New Name")
        """
        try:
            cursor = self.connection.cursor()

            query = """
                UPDATE vocabulary 
                SET group_name = ? 
                WHERE group_name = ?
            """

            cursor.execute(query, (new_name, old_name))
            self.connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error renaming group: {e}")
            self.connection.rollback()
            return False

    def delete_group(self, group_name: str, reassign_to: str = None) -> bool:
        """
        Delete a group and optionally reassign its words.

        Args:
            group_name: Group to delete
            reassign_to: Optional group to reassign words to (None = set to empty)

        Returns:
            True if successful

        Usage:
            # Remove group, set words to no group
            db.delete_group("Old Group")

            # Remove group, reassign words
            db.delete_group("Old Group", "New Group")
        """
        try:
            cursor = self.connection.cursor()

            query = """
                UPDATE vocabulary 
                SET group_name = ? 
                WHERE group_name = ?
            """

            new_value = reassign_to if reassign_to else ""
            cursor.execute(query, (new_value, group_name))
            self.connection.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error deleting group: {e}")
            self.connection.rollback()
            return False

    def get_words_by_group(self, group_name: str) -> list:
        """
        Get all words in a specific group.

        Args:
            group_name: Group name to filter by

        Returns:
            List of word tuples in that group

        Usage:
            words = db.get_words_by_group("Animals")
        """
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT engWord, hebWord, difficulty, group_name
                FROM vocabulary 
                WHERE group_name = ?
                ORDER BY engWord
            """

            cursor.execute(query, (group_name,))
            return cursor.fetchall()

        except Exception as e:
            print(f"Error getting words by group: {e}")
            return []

    def get_group_statistics(self) -> dict:
        """
        Get statistics about groups.

        Returns:
            Dictionary with group stats

        Usage:
            stats = db.get_group_statistics()
            # Returns: {"Greetings": 15, "Animals": 23, ...}
        """
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT group_name, COUNT(*) as count
                FROM vocabulary
                WHERE group_name IS NOT NULL AND group_name != ''
                GROUP BY group_name
                ORDER BY count DESC
            """

            cursor.execute(query)
            results = cursor.fetchall()

            return {row[0]: row[1] for row in results}

        except Exception as e:
            print(f"Error getting group statistics: {e}")
            return {}

    # ==================== Example: Complete DatabaseManager class ====================

    """
    Here's how these methods integrate into your existing DatabaseManager:

    class DatabaseManager:
        def __init__(self, db_path):
            self.connection = sqlite3.connect(db_path)
            self.create_tables()

        def create_tables(self):
            cursor = self.connection.cursor()

            # Main words table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    english TEXT NOT NULL,
                    hebrew TEXT UNIQUE NOT NULL,
                    difficulty TEXT NOT NULL,
                    group_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Optional: Separate groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.connection.commit()

        def get_full_data(self):
            # Your existing method
            cursor = self.connection.cursor()
            cursor.execute('SELECT english, hebrew, difficulty, group_name FROM words')
            return cursor.fetchall()

        def get_word_details(self, english_word):
            # Your existing method
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT id, hebrew, english, difficulty, group_name FROM words WHERE english = ?',
                (english_word,)
            )
            return cursor.fetchone()

        def update_difficulty(self, hebrew_word, new_difficulty):
            # Your existing method
            cursor = self.connection.cursor()
            cursor.execute(
                'UPDATE words SET difficulty = ? WHERE hebrew = ?',
                (new_difficulty, hebrew_word)
            )
            self.connection.commit()

        # ADD THE NEW METHODS HERE:
        # - update_group()
        # - get_all_groups()
        # - create_group()
        # - rename_group()
        # - delete_group()
        # - get_words_by_group()
        # - get_group_statistics()
    """

    # ==================== Database Schema Example ====================

    """
    Recommended table structure:

    CREATE TABLE words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT NOT NULL,
        hebrew TEXT UNIQUE NOT NULL,
        difficulty TEXT NOT NULL CHECK(difficulty IN ('EASY', 'MEDIUM', 'HARD')),
        group_name TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_name) REFERENCES groups(name) ON UPDATE CASCADE
    );

    CREATE TABLE groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        color TEXT,  -- Optional: for UI color coding
        icon TEXT,   -- Optional: for UI icons
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX idx_words_group ON words(group_name);
    CREATE INDEX idx_words_difficulty ON words(difficulty);
    """


