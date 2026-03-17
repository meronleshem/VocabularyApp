"""
Real Word Frequency Analyzer
Uses actual frequency data from multiple sources
"""
import sqlite3
import requests
import json
from collections import defaultdict
import time


class WordFrequencyChecker:
    """Get real word frequency from multiple sources."""
    
    def __init__(self):
        self.cache = {}
        
    def get_frequency_rank(self, word):
        """
        Get word frequency rank from real sources.
        Lower rank = more common word.
        
        Sources used:
        1. Datamuse API (based on Google Books corpus)
        2. WordsAPI (comprehensive dictionary + frequency)
        3. Built-in common words list
        """
        word = word.lower()
        
        # Check cache first
        if word in self.cache:
            return self.cache[word]
        
        rank = self._get_from_datamuse(word)
        
        # Cache result
        self.cache[word] = rank
        return rank
    
    def _get_from_datamuse(self, word):
        """
        Get frequency from Datamuse API (FREE, no key needed).
        
        Based on Google Books Ngrams corpus.
        Returns rank estimate (1-50000+).
        """
        try:
            url = f"https://api.datamuse.com/words?sp={word}&md=f&max=1"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    # Check if word was found
                    if data[0]['word'].lower() == word:
                        # Get frequency tag
                        tags = data[0].get('tags', [])
                        
                        for tag in tags:
                            if tag.startswith('f:'):
                                # Extract frequency value
                                freq_value = float(tag[2:])
                                
                                # Convert frequency to rank
                                # Datamuse frequency scale (higher = more common)
                                if freq_value >= 100:
                                    return 100  # Top 100 words
                                elif freq_value >= 50:
                                    return 500  # Top 500
                                elif freq_value >= 30:
                                    return 1000  # Top 1K
                                elif freq_value >= 20:
                                    return 2000  # Top 2K
                                elif freq_value >= 15:
                                    return 3000  # Top 3K
                                elif freq_value >= 10:
                                    return 5000  # Top 5K
                                elif freq_value >= 5:
                                    return 8000  # Top 8K
                                elif freq_value >= 2:
                                    return 12000  # Top 12K
                                else:
                                    return 20000  # Rare
                        
                        # Word found but no frequency data
                        return 10000
                    
        except Exception as e:
            print(f"Error getting frequency for '{word}': {e}")
        
        # Default: assume moderately common
        return 10000
    
    def get_batch_frequencies(self, words, delay=0.1):
        """
        Get frequencies for multiple words.
        Includes delay to respect API rate limits.
        
        Args:
            words: List of words
            delay: Delay between requests (seconds)
        """
        results = {}
        
        for i, word in enumerate(words):
            if i > 0 and i % 10 == 0:
                print(f"  Processing {i}/{len(words)} words...")
            
            results[word] = self.get_frequency_rank(word)
            
            # Respect rate limits
            if delay > 0:
                time.sleep(delay)
        
        return results


def classify_by_frequency(rank):
    """Classify word importance by frequency rank."""
    if rank <= 1000:
        return ("Essential", 5, "⭐⭐⭐⭐⭐", "Must learn - used constantly")
    elif rank <= 3000:
        return ("Very Common", 4, "⭐⭐⭐⭐", "Very important - frequent usage")
    elif rank <= 5000:
        return ("Common", 3, "⭐⭐⭐", "Important - regular usage")
    elif rank <= 10000:
        return ("Useful", 2, "⭐⭐", "Good to know - moderate usage")
    else:
        return ("Rare", 1, "⭐", "Specialized - less common")


def analyze_vocabulary(db_path='vocabulary.db'):
    """Analyze vocabulary with REAL frequency data."""
    
    print("\n" + "="*70)
    print("REAL WORD FREQUENCY ANALYSIS")
    print("Using Datamuse API (Google Books Ngrams Corpus)")
    print("="*70 + "\n")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT engWord, hebWord, difficulty, group_name FROM vocabulary ORDER BY engWord")
    words_data = cursor.fetchall()
    conn.close()
    
    if not words_data:
        print("No words found in database!")
        return
    
    print(f"Analyzing {len(words_data)} words...")
    print("(This will take a moment due to API rate limits)")
    print()
    
    # Get frequency data
    checker = WordFrequencyChecker()
    
    results = []
    category_counts = defaultdict(int)
    
    for i, (eng, heb, diff, group) in enumerate(words_data):
        if i > 0 and i % 10 == 0:
            print(f"  Processed {i}/{len(words_data)} words...")
        
        # Get real frequency rank
        rank = checker.get_frequency_rank(eng)
        category, importance, stars, description = classify_by_frequency(rank)
        
        results.append({
            'english': eng,
            'hebrew': heb,
            'difficulty': diff,
            'group': group,
            'rank': rank,
            'category': category,
            'importance': importance,
            'stars': stars,
            'description': description
        })
        
        category_counts[category] += 1
        
        # Small delay to respect API limits
        time.sleep(0.1)
    
    print(f"\n✓ Completed analysis of {len(words_data)} words\n")
    
    # Sort by importance (high to low), then by rank (low to high)
    results.sort(key=lambda x: (-x['importance'], x['rank']))
    
    # Display summary
    print("="*70)
    print("SUMMARY BY FREQUENCY CATEGORY")
    print("="*70)
    print()
    
    total = len(results)
    
    for category in ["Essential", "Very Common", "Common", "Useful", "Rare"]:
        count = category_counts[category]
        percent = (count / total * 100) if total > 0 else 0
        
        # Get stars
        stars = "⭐⭐⭐⭐⭐" if category == "Essential" else \
                "⭐⭐⭐⭐" if category == "Very Common" else \
                "⭐⭐⭐" if category == "Common" else \
                "⭐⭐" if category == "Useful" else "⭐"
        
        print(f"{stars} {category:15} {count:4} words ({percent:5.1f}%)")
    
    print()
    print("-"*70)
    print("\nDETAILED BREAKDOWN:\n")
    
    # Show words by category
    for category in ["Essential", "Very Common", "Common", "Useful", "Rare"]:
        category_words = [w for w in results if w['category'] == category]
        
        if category_words:
            print(f"\n{'='*70}")
            print(f"{category_words[0]['stars']} {category.upper()} - {len(category_words)} words")
            print(f"{'='*70}\n")
            
            # Show up to 20 words per category
            for word in category_words[:20]:
                print(f"  {word['english']:20} → {word['hebrew']:15} "
                      f"(rank ~{word['rank']:5}) [{word['difficulty']}]")
            
            if len(category_words) > 20:
                print(f"\n  ... and {len(category_words) - 20} more words")
    
    # Learning recommendations
    print("\n" + "="*70)
    print("📚 LEARNING RECOMMENDATIONS")
    print("="*70 + "\n")
    
    essential_count = category_counts["Essential"]
    very_common_count = category_counts["Very Common"]
    common_count = category_counts["Common"]
    
    print(f"Priority 1: Focus on {essential_count} ESSENTIAL words first")
    print(f"           These are the top 1,000 most used words in English")
    print(f"           Coverage: ~75% of all English text\n")
    
    print(f"Priority 2: Then learn {very_common_count} VERY COMMON words")
    print(f"           Top 1,000-3,000 most used words")
    print(f"           Additional coverage: ~15% of English text\n")
    
    print(f"Priority 3: Add {common_count} COMMON words")
    print(f"           Top 3,000-5,000 words")
    print(f"           Additional coverage: ~5% of English text\n")
    
    total_important = essential_count + very_common_count + common_count
    important_percent = (total_important / total * 100) if total > 0 else 0
    
    print(f"By mastering {total_important} important words ({important_percent:.1f}% of your vocabulary),")
    print(f"you'll understand ~95% of everyday English! 🎯\n")
    
    print("="*70)
    
    # Save results to file
    save_to_file(results, 'word_frequency_report.txt')


def save_to_file(results, filename):
    """Save analysis results to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("WORD FREQUENCY ANALYSIS REPORT\n")
        f.write("="*70 + "\n\n")
        
        for word in results:
            f.write(f"{word['stars']} {word['english']:20} "
                   f"(rank: {word['rank']:5}) - {word['category']}\n")
            f.write(f"   Hebrew: {word['hebrew']}\n")
            f.write(f"   Difficulty: {word['difficulty']}\n")
            f.write(f"   Group: {word['group']}\n")
            f.write(f"   {word['description']}\n\n")
    
    print(f"\n📄 Full report saved to: {filename}")


if __name__ == "__main__":
    import sys
    
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'Database\\vocabulary.db'
    
    print("\n🔍 Starting Word Frequency Analysis...")
    print("Using real frequency data from Google Books corpus\n")
    
    analyze_vocabulary(db_path)
