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
        """Add a new word to the database."""
        if self.is_word_exists(eng_word):
            print(f"{eng_word} is already exists. Abort adding")
            return False

        heb_word = translate_to_heb(eng_word)
        if heb_word is None:
            print(f"{eng_word} is not a valid word. Abort adding")
            return False

        examples = get_word_examples(eng_word)

        # Let SQLite auto-generate the ID - don't specify it
        word_data = (eng_word.lower(), heb_word, examples, Difficulty.NEW_WORD.name, group_name)

        self.cursor.execute(
            f"INSERT INTO {self.table_name} "
            f"(engWord, hebWord, examples, difficulty, group_name) "
            f"VALUES (?, ?, ?, ?, ?)",
            word_data
        )

        self.connection.commit()
        print(f"{eng_word} was added!")
        return True

    def add_from_file(self, filepath):
        words_to_add = read_words_from_file(filepath)

        pack_size = 40
        curr_pack = 2
        curr_pack_num = 0
        for word in words_to_add:
            group_name = f"The Will of The Many {curr_pack}"
            if self.add_word(word, group_name) is True:
                curr_pack_num += 1
            if curr_pack_num == pack_size:
                curr_pack += 1
                curr_pack_num = 0

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

    def update_examples(self, eng_word: str, examples: str) -> bool:
        """Update examples for a word."""
        try:
            self.cursor.execute(
                "UPDATE vocabulary SET examples = ? WHERE engWord = ?",
                (examples, eng_word)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating examples: {e}")
            return False

    def add_highlight_words_from_pdf(self, filepath):
        words_to_add = extract_highlight_words_from_pdf(filepath)

        pack_size = 40
        curr_pack = 1
        curr_pack_num = 0
        for word in words_to_add:
            group_name = f"Project Hail Mary {curr_pack}"
            if self.add_word(word, group_name) is True:
                curr_pack_num += 1
            if curr_pack_num == pack_size:
                curr_pack += 1
                curr_pack_num = 0

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

    def get_words_with_examples(self):
        query = """
            SELECT engWord, hebWord, difficulty, examples, group_name 
            FROM vocabulary 
            WHERE examples IS NOT NULL AND examples != ''
        """
        self.cursor.execute(query)
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

    """
    Additional Methods for DatabaseManager

    Add these methods to your existing DatabaseManager class to get group statistics.
    """

    def print_group_statistics(self):
        try:
            query = """
                SELECT group_name, COUNT(*) as word_count
                FROM vocabulary
                WHERE group_name IS NOT NULL AND group_name != ''
                GROUP BY group_name
                ORDER BY word_count DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                print("No groups found in database.")
                return

            # Calculate totals
            total_words = sum(count for _, count in results)
            total_groups = len(results)

            # Print header
            print()
            print("=" * 70)
            print("WORD GROUPS STATISTICS")
            print("=" * 70)
            print()
            print(f"Total Groups: {total_groups}")
            print(f"Total Words:  {total_words}")
            print()

            # Print table
            print(f"{'Group Name':<45} {'Words':>8}  {'%':>8}")
            print("-" * 70)

            for group_name, word_count in results:
                percentage = (word_count / total_words * 100) if total_words > 0 else 0
                display_name = group_name[:44] if len(group_name) > 44 else group_name
                print(f"{display_name:<45} {word_count:>8}  {percentage:>7.1f}%")

            # Print footer
            print("-" * 70)
            print(f"{'TOTAL':<45} {total_words:>8}  {100.0:>7.1f}%")
            print()

        except Exception as e:
            print(f"Error: {e}")

    def get_group_word_counts(self):
        try:
            query = """
                SELECT group_name, COUNT(*) as word_count
                FROM vocabulary
                WHERE group_name IS NOT NULL AND group_name != ''
                GROUP BY group_name
                ORDER BY word_count DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            return {group: count for group, count in results}

        except Exception as e:
            print(f"Error getting group word counts: {e}")
            return {}

    def print_group_statistics_with_difficulty(self):
        try:
            query = """
                SELECT 
                    group_name,
                    COUNT(*) as total,
                    SUM(CASE WHEN difficulty = 'NEW_WORD' THEN 1 ELSE 0 END) as new_word,
                    SUM(CASE WHEN difficulty = 'EASY' THEN 1 ELSE 0 END) as easy,
                    SUM(CASE WHEN difficulty = 'MEDIUM' THEN 1 ELSE 0 END) as medium,
                    SUM(CASE WHEN difficulty = 'HARD' THEN 1 ELSE 0 END) as hard
                FROM vocabulary
                WHERE group_name IS NOT NULL AND group_name != ''
                GROUP BY group_name
                ORDER BY total DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                print("No groups found.")
                return

            print()
            print("=" * 90)
            print("WORD GROUPS - DIFFICULTY BREAKDOWN")
            print("=" * 90)
            print()

            # Header
            print(f"{'Group Name':<35} {'Total':>7} {'New':>6} {'Easy':>6} {'Med':>6} {'Hard':>6}")
            print("-" * 90)

            total_all = 0
            total_new = 0
            total_easy = 0
            total_medium = 0
            total_hard = 0

            for row in results:
                group_name, total, new, easy, medium, hard = row
                display_name = group_name[:34] if len(group_name) > 34 else group_name

                print(f"{display_name:<35} {total:>7} {new:>6} {easy:>6} {medium:>6} {hard:>6}")

                total_all += total
                total_new += new
                total_easy += easy
                total_medium += medium
                total_hard += hard

            # Footer
            print("-" * 90)
            print(f"{'TOTAL':<35} {total_all:>7} {total_new:>6} {total_easy:>6} {total_medium:>6} {total_hard:>6}")
            print()

        except Exception as e:
            print(f"Error: {e}")

    def get_group_info(self, group_name):
        try:
            # Total words
            query_total = """
                SELECT COUNT(*) FROM vocabulary 
                WHERE group_name = ?
            """
            self.cursor.execute(query_total, (group_name,))
            total_words = self.cursor.fetchone()[0]

            # Difficulty breakdown
            query_diff = """
                SELECT difficulty, COUNT(*) 
                FROM vocabulary 
                WHERE group_name = ?
                GROUP BY difficulty
            """
            self.cursor.execute(query_diff, (group_name,))
            difficulty_breakdown = dict(self.cursor.fetchall())

            # With/without examples
            query_examples = """
                SELECT 
                    COUNT(CASE WHEN examples IS NOT NULL AND examples != '' THEN 1 END) as with_examples,
                    COUNT(CASE WHEN examples IS NULL OR examples = '' THEN 1 END) as without_examples
                FROM vocabulary
                WHERE group_name = ?
            """
            self.cursor.execute(query_examples, (group_name,))
            result = self.cursor.fetchone()

            return {
                'total_words': total_words,
                'difficulty_breakdown': difficulty_breakdown,
                'with_examples': result[0] if result else 0,
                'without_examples': result[1] if result else 0
            }

        except Exception as e:
            print(f"Error getting group info: {e}")
            return None

    def delete_word(self, english_word: str) -> bool:
        try:
            query = "DELETE FROM vocabulary WHERE engWord = ?"
            self.cursor.execute(query, (english_word,))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"✓ Successfully deleted: {english_word}")
                return True
            else:
                print(f"✗ Word not found: {english_word}")
                return False

        except Exception as e:
            print(f"✗ Error deleting word: {e}")
            self.connection.rollback()
            return False


