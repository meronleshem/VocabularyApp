"""
Find Word Families - Script to identify words with the same root

This script analyzes your vocabulary database and groups words by their stem/root.
For example: breed, breeding, breeds all share the root "breed"
"""
import sqlite3
from collections import defaultdict
import re


def get_word_stem(word):
    """
    Get the base form (stem) of a word by removing common suffixes.
    
    This is a simplified stemming - for better results, you could use
    the nltk library's PorterStemmer or Snowball stemmer.
    """
    word = word.lower()
    
    # Common suffixes to try removing (in order of priority)
    suffixes = [
        'ing',      # breeding -> breed
        'ed',       # jumped -> jump
        's',        # breeds -> breed
        'es',       # watches -> watch
        'er',       # faster -> fast
        'est',      # fastest -> fast
        'ly',       # quickly -> quick
        'ness',     # happiness -> happi
        'tion',     # creation -> creat
        'ment',     # movement -> move
        'ity',      # clarity -> clar
        'ful',      # beautiful -> beauti
        'less',     # hopeless -> hope
        'able',     # readable -> read
        'ible',     # visible -> vis
    ]
    
    # Try each suffix
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    
    return word


def find_word_families(db_path='vocabulary.db'):
    """
    Find and display word families from the database.
    
    Args:
        db_path: Path to the SQLite database
    """
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all English words
    cursor.execute("SELECT engWord FROM vocabulary ORDER BY engWord")
    words = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    if not words:
        print("No words found in database!")
        return
    
    # Group words by stem
    families = defaultdict(list)
    
    for word in words:
        stem = get_word_stem(word)
        families[stem].append(word)
    
    # Filter to only show families with 2+ words
    word_families = {stem: words for stem, words in families.items() if len(words) > 1}
    
    # Display results
    print("=" * 70)
    print("WORD FAMILIES FOUND IN YOUR VOCABULARY")
    print("=" * 70)
    print()
    
    if not word_families:
        print("No word families found.")
        print("(A word family has 2+ words with the same root)")
        return
    
    # Sort by family size (largest first)
    sorted_families = sorted(word_families.items(), key=lambda x: len(x[1]), reverse=True)
    
    total_families = len(sorted_families)
    total_words_in_families = sum(len(words) for words in word_families.values())
    
    print(f"Found {total_families} word families containing {total_words_in_families} words total")
    print()
    print("-" * 70)
    
    for i, (stem, family_words) in enumerate(sorted_families, 1):
        print(f"\n{i}. Root: '{stem}' ({len(family_words)} words)")
        print(f"   Words: {', '.join(family_words)}")
    
    print()
    print("=" * 70)
    print(f"Summary: {total_families} families, {total_words_in_families} words")
    print("=" * 70)


def find_word_families_advanced(db_path='vocabulary.db'):
    """
    Advanced version using NLTK for better stemming.
    
    Requires: pip install nltk
    """
    try:
        import nltk
        from nltk.stem import PorterStemmer
        
        # Download required data (first time only)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        stemmer = PorterStemmer()
        
    except ImportError:
        print("NLTK not installed. Using basic stemming.")
        print("For better results, run: pip install nltk")
        find_word_families(db_path)
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all words with their details
    cursor.execute("""
        SELECT engWord, hebWord, difficulty, group_name 
        FROM vocabulary 
        ORDER BY engWord
    """)
    words_data = cursor.fetchall()
    conn.close()
    
    if not words_data:
        print("No words found in database!")
        return
    
    # Group words by stem using NLTK
    families = defaultdict(list)
    
    for eng, heb, diff, group in words_data:
        stem = stemmer.stem(eng.lower())
        families[stem].append({
            'english': eng,
            'hebrew': heb,
            'difficulty': diff,
            'group': group
        })
    
    # Filter to families with 2+ words
    word_families = {stem: words for stem, words in families.items() if len(words) > 1}
    
    # Display results
    print("=" * 70)
    print("WORD FAMILIES FOUND (Advanced Stemming)")
    print("=" * 70)
    print()
    
    if not word_families:
        print("No word families found.")
        return
    
    sorted_families = sorted(word_families.items(), key=lambda x: len(x[1]), reverse=True)
    
    total_families = len(sorted_families)
    total_words = sum(len(words) for words in word_families.values())
    
    print(f"Found {total_families} word families containing {total_words} words")
    print()
    print("-" * 70)
    
    for i, (stem, family_words) in enumerate(sorted_families, 1):
        print(f"\n{i}. Root: '{stem}' ({len(family_words)} words)")
        
        for word_info in family_words:
            print(f"   • {word_info['english']:<15} → {word_info['hebrew']:<15} "
                  f"[{word_info['difficulty']:<10}] ({word_info['group']})")
    
    print()
    print("=" * 70)
    print(f"Summary: {total_families} families, {total_words} words")
    print("=" * 70)


def find_exact_prefix_families(db_path='vocabulary.db', min_prefix_length=4):
    """
    Find word families by exact prefix matching.
    More conservative than stemming.
    
    Example: 'breed' matches 'breeding', 'breeds' (starts with 'breed')
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT engWord FROM vocabulary ORDER BY engWord")
    words = [row[0].lower() for row in cursor.fetchall()]
    conn.close()
    
    if not words:
        print("No words found!")
        return
    
    # Find families
    families = defaultdict(list)
    
    for i, word1 in enumerate(words):
        if len(word1) < min_prefix_length:
            continue
        
        family = [word1]
        
        for word2 in words[i+1:]:
            # Check if word2 starts with word1 (or vice versa)
            if word2.startswith(word1) or word1.startswith(word2):
                if word2 not in family:
                    family.append(word2)
        
        if len(family) > 1:
            # Use shortest word as the root
            root = min(family, key=len)
            for word in family:
                if word not in families[root]:
                    families[root].append(word)
    
    # Remove duplicates and sort
    unique_families = {}
    seen_words = set()
    
    for root, family in families.items():
        family_set = set(family)
        if not family_set.issubset(seen_words):
            unique_families[root] = sorted(family)
            seen_words.update(family_set)
    
    # Display
    print("=" * 70)
    print("WORD FAMILIES (Exact Prefix Matching)")
    print("=" * 70)
    print()
    
    if not unique_families:
        print("No word families found with exact prefix matching.")
        return
    
    sorted_families = sorted(unique_families.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"Found {len(sorted_families)} families")
    print()
    
    for i, (root, family) in enumerate(sorted_families, 1):
        print(f"{i}. {root} → {', '.join(family)}")
    
    print()
    print("=" * 70)


# ==================== Main Script ====================

if __name__ == "__main__":
    import sys
    
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'Database\\vocabulary.db'
    
    print("\n🔍 WORD FAMILY FINDER")
    print("=" * 70)
    print()
    print("Choose a method:")
    print("1. Basic Stemming (fast, built-in)")
    print("2. Advanced Stemming (requires NLTK, more accurate)")
    print("3. Exact Prefix Matching (conservative, no stemming)")
    print()
    
    choice = input("Enter choice (1-3, default=1): ").strip() or "1"
    
    print()
    
    if choice == "1":
        find_word_families(db_path)
    elif choice == "2":
        find_word_families_advanced(db_path)
    elif choice == "3":
        find_exact_prefix_families(db_path)
    else:
        print("Invalid choice. Using basic stemming.")
        find_word_families(db_path)

    input("Enter any to exit...")
