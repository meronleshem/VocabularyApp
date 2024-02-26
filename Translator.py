import requests
from bs4 import BeautifulSoup


def translate_to_heb(word):
    # Combine the base URL and additional string
    base_url = 'https://www.morfix.co.il/'
    div_class = 'normal_translation_div'
    url = f"{base_url}{word}"

    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific div element with the specified class
        specific_div = soup.find('div', class_=div_class)

        # Check if the div element was found
        if specific_div:
            # Print the content of the div element
            return specific_div.text.strip()
        else:
            print(f"Error: The div with class '{div_class}' was not found on the page.")
    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
