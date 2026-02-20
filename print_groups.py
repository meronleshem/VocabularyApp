"""
Print Group Statistics - Simple Script

Run this to see how many words are in each group.

Usage:
    python print_groups.py
"""
from Database.DatabaseManager import DatabaseManager


def print_group_statistics(db):
    """Print statistics about word groups."""
    
    try:
        # Query to get word count per group
        query = """
            SELECT group_name, COUNT(*) as word_count
            FROM vocabulary
            WHERE group_name IS NOT NULL AND group_name != ''
            GROUP BY group_name
            ORDER BY word_count DESC
        """
        db.cursor.execute(query)
        results = db.cursor.fetchall()
        
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
            # Truncate long names
            display_name = group_name[:44] if len(group_name) > 44 else group_name
            print(f"{display_name:<45} {word_count:>8}  {percentage:>7.1f}%")
        
        # Print footer
        print("-" * 70)
        print(f"{'TOTAL':<45} {total_words:>8}  {100.0:>7.1f}%")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


def print_group_statistics_with_difficulty(db):
    """Print statistics with difficulty breakdown."""
    
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
        db.cursor.execute(query)
        results = db.cursor.fetchall()
        
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


if __name__ == "__main__":
    # Create database connection
    db = DatabaseManager()
    
    # Print basic statistics
    print_group_statistics(db)
    
    # Print with difficulty breakdown
    print_group_statistics_with_difficulty(db)
    
    # Close connection
    db.close_db_connection()
    input("Press Enter to exit...")
