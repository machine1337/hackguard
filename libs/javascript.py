import requests
from bs4 import BeautifulSoup
import re

def extract_js_links(url, js_file):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    js_links = []
    for script in soup.find_all('script'):
        src = script.get('src')
        if src and src.endswith('.js'):
            js_links.append(src)

    with open(js_file, 'w') as file:
        for link in js_links:
            file.write(link + '\n')




