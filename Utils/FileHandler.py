from typing import List, Tuple
import fitz  # install with 'pip install pymupdf'
import string

compressed_alphabet = string.ascii_lowercase + string.ascii_uppercase
alphabet_list = [char for char in compressed_alphabet]


def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence


def handle_page(page):
    wordlist = page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def extract_highlight_words_from_pdf(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return remove_symbols_from_list(highlights)


def remove_symbols_from_list(word_list):
    cleaned_list = [remove_symbols(word) for word in word_list]
    return cleaned_list


def remove_symbols(word):
    # Remove symbols from the start of the word
    while word and word[0] not in alphabet_list:
        word = word[1:]

    # Remove symbols from the end of the word
    while word and word[-1] not in alphabet_list:
        word = word[:-1]

    return word


def read_words_from_file():
    words_to_add = []
    file_name = "wordsToAdd.txt"
    with open(file_name, 'r') as file:
        for line in file:
            words_to_add.append(line.strip())

    return words_to_add

