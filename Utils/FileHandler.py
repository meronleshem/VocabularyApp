from typing import List, Tuple
import fitz  # install with 'pip install pymupdf'
import string

compressed_alphabet = string.ascii_lowercase + string.ascii_uppercase
alphabet_list = [char for char in compressed_alphabet]


def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    sentence = ""
    if points:
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
            word = _parse_highlight(annot, wordlist)
            clean_word = remove_symbols(word)
            highlights.append(clean_word)
        annot = annot.next
    return highlights


def get_chapter_by_page_num(chapters_list, page_num):
    for chapter, first_page, last_page in chapters_list:
        if first_page <= page_num <= last_page:
            return chapter

    return ""


def extract_highlight_words_from_pdf(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        highlights += handle_page(page)

    pack_size = 40
    packed_list = [(word, pack_num // pack_size + 1) for pack_num, word in enumerate(highlights)]
    return packed_list


def remove_symbols(word):
    while word and word[0] not in alphabet_list:
        word = word[1:]

    while word and word[-1] not in alphabet_list:
        word = word[:-1]

    return word


def extract_chapters_by_font_size(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    chapters = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        font_size = span["size"]

                        # Assuming headings are the largest text on the page
                        if font_size > 15 and len(text) > 0:  # Adjust the font size threshold as needed
                            chapters.append((page_num + 1, text, font_size))

    return chapters


def get_chapter_list_with_page_range(pdf_path):
    chapters = extract_chapters_by_font_size(pdf_path)

    chapters_list_page_range = []
    for i in range(len(chapters) - 1):
        page1, text1, size1 = chapters[i]
        page2, text2, size2 = chapters[i + 1]

        if page1 == page2:
            continue
        chapters_list_page_range.append((text1, page1, page2 - 1))

    return chapters_list_page_range


def read_words_from_file(filepath):

    words_to_add = []
    with open(filepath, 'r') as file:
        for line in file:
            words_to_add.append(line.strip())

    return words_to_add

