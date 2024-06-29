import requests
from bs4 import BeautifulSoup


def translate_to_heb(eng_word):
    base_url = 'https://www.morfix.co.il/'
    div_class = 'normal_translation_div'
    url = f"{base_url}{eng_word}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        specific_div = soup.find('div', class_=div_class)

        if specific_div:
            return specific_div.text.strip()
        else:
            print(f"Error: The div with class '{div_class}' was not found on the page.")
    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")

def get_word_examples(eng_word):
    base_url = 'https://www.morfix.co.il/'
    span_class = 'Translation_ulFooter_enTohe'
    url = f"{base_url}{eng_word}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        specific_ul = soup.find('ul', class_=span_class)

        if specific_ul:
            li_elements = specific_ul.find_all('li')
            first_three_li = li_elements[:3]
            return '\n'.join([li.get_text() for li in first_three_li])
        else:
            print(f"Error with {eng_word}: The div with class '{span_class}' was not found on the page.")
            return None
    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
        return None
