
def read_words_from_file():
    words_to_add = []
    file_name = "wordsToAdd.txt"
    with open(file_name, 'r') as file:
        for line in file:
            words_to_add.append(line.strip())

    return words_to_add

