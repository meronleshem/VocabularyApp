# import os
# from typing import Optional, List
#
#
# def generate_examples_dictionary(word: str) -> str:
#     try:
#         import requests
#
#         # Use Free Dictionary API
#         url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#         response = requests.get(url, timeout=5)
#
#         if response.status_code != 200:
#             return f"No examples found for '{word}'"
#
#         data = response.json()
#         examples = []
#
#         # Extract examples from definitions
#         for entry in data:
#             for meaning in entry.get('meanings', []):
#                 for definition in meaning.get('definitions', []):
#                     example = definition.get('example')
#                     if example:
#                         examples.append(example)
#
#         if examples:
#             # Return up to 5 examples
#             return "\n".join(examples[:5])
#         else:
#             return f"No examples found for '{word}'"
#
#     except ImportError:
#         return "Error: requests not installed. Run: pip install requests"
#     except Exception as e:
#         return f"Error: {e}"

"""
Example Generator - SIMPLIFIED VERSION

Only includes methods that actually work well:
1. Dictionary API (FREE, recommended)
2. OpenAI GPT (paid, excellent quality)
3. Anthropic Claude (paid, excellent quality)
4. Template fallback (offline, always works)
"""
import os
from typing import Optional

"""
Example Generator - Simple & Clean

Only 2 methods (both FREE):
1. Dictionary.com scraping (BEST)
2. Free Dictionary API (fallback)
"""
import re
from typing import Optional


# ==================== Dictionary.com Scraper ====================

def scrape_dictionary_com_examples(word: str) -> Optional[str]:
    """
    Scrape example sentences from dictionary.com "Example Sentences" section.

    ✅ FREE - No API key needed
    ✅ HIGH QUALITY - Real example sentences
    ✅ With sources (BBC, Literature, etc.)

    Args:
        word: English word

    Returns:
        Example sentences (up to 3), one per line

    Requires:
        pip install requests beautifulsoup4 --break-system-packages
    """
    try:
        import requests
        from bs4 import BeautifulSoup

        url = f"https://www.dictionary.com/browse/{word.lower()}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        print(f"Fetching from dictionary.com: {word}")
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        examples = []

        # Find the "Example Sentences" section
        # Look for heading that says "Example Sentences"
        example_heading = soup.find(['h2', 'h3', 'h4'], string=re.compile(r'Example Sentences?', re.IGNORECASE))

        if example_heading:
            print("✓ Found 'Example Sentences' section")

            # Get the container after the heading
            container = example_heading.find_parent()

            if container:
                # Find all example sentence blocks
                # They are usually in <p> or <div> tags after the heading

                # Method 1: Look for siblings after the heading
                for sibling in example_heading.find_next_siblings():
                    # Look for text in paragraphs or divs
                    text_elements = sibling.find_all(['p', 'div', 'span'])

                    for elem in text_elements:
                        text = elem.get_text().strip()

                        # Filter: should be a sentence (10-300 chars, contains the word)
                        if text and 10 < len(text) < 300:
                            # Remove extra whitespace
                            text = re.sub(r'\s+', ' ', text)

                            # Check if it contains the word (case-insensitive)
                            if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
                                # Remove source labels like "From BBC" at the end
                                text = re.sub(r'\s*From\s+\w+.*$', '', text)

                                if text and text not in examples:
                                    examples.append(text)

                                    if len(examples) >= 7:
                                        break

                    if len(examples) >= 7:
                        break

        # Method 2: If section not found, look for any examples on the page
        if not examples:
            print("Trying alternative method...")

            # Look for common example containers
            example_containers = soup.find_all(['div', 'p'], class_=re.compile(r'example|sentence', re.IGNORECASE))

            for container in example_containers:
                text = container.get_text().strip()

                if text and 10 < len(text) < 300:
                    text = re.sub(r'\s+', ' ', text)

                    if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
                        text = re.sub(r'\s*From\s+\w+.*$', '', text)

                        if text and text not in examples:
                            examples.append(text)

                            if len(examples) >= 7:
                                break

        if examples:
            print(f"✓ Found {len(examples)} examples")
            return "\n".join(examples)
        else:
            print("✗ No examples found")
            return None

    except ImportError:
        print("Error: beautifulsoup4 not installed")
        print("Install: pip install beautifulsoup4 --break-system-packages")
        return None
    except Exception as e:
        print(f"Error scraping dictionary.com: {e}")
        return None


# ==================== Free Dictionary API (Fallback) ====================

def scrape_free_dictionary_api(word: str) -> Optional[str]:
    """
    Get examples from free dictionary API (fallback).

    ✅ FREE
    ✅ No installation (only needs requests)

    Args:
        word: English word

    Returns:
        Example sentences or None

    Requires:
        pip install requests --break-system-packages
    """
    try:
        import requests

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        examples = []

        for entry in data:
            for meaning in entry.get('meanings', []):
                for definition in meaning.get('definitions', []):
                    example = definition.get('example')
                    if example:
                        examples.append(example)

        if examples:
            return "\n".join(examples[:3])
        else:
            return None

    except ImportError:
        print("Error: requests not installed")
        print("Install: pip install requests --break-system-packages")
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None


# ==================== Main Function ====================

def get_word_examples_ai(word: str) -> str:
    """
    Get example sentences for a word.

    Tries:
        1. Dictionary.com (best quality)
        2. Free Dictionary API (fallback)
        3. Simple template (if all else fails)

    Args:
        word: English word

    Returns:
        Example sentences (3 sentences, one per line)
    """
    print(f"Generating examples for '{word}'...")

    # 1. Try dictionary.com first (best)
    result = scrape_dictionary_com_examples(word)
    if result:
        print("✓ Using Dictionary.com")
        return result

    # 2. Try free API
    result = scrape_free_dictionary_api(word)
    if result:
        print("✓ Using Free Dictionary API")
        return result

    # 3. Fallback to simple template
    print("⚠ Using template fallback")
    import random

    templates = [
        f"The {word} was quite impressive.",
        f"She studied the {word} carefully.",
        f"Everyone noticed the {word}.",
    ]

    return "\n".join(random.sample(templates, 3))


# ==================== Test ====================

if __name__ == "__main__":
    """Test the scraper."""

    print("=" * 70)
    print("Dictionary.com Example Scraper - Test")
    print("=" * 70)
    print()

    test_words = ["afoot", "ephemeral", "foraging", "serendipity"]

    for word in test_words:
        print(f"\n{'=' * 70}")
        print(f"Word: {word}")
        print('=' * 70)

        examples = get_word_examples_ai(word)

        print("\nResult:")
        print(examples)
        print()
