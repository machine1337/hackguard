import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

visited_urls = set()

def crawl_website(url, user_agent):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            visited_urls.add(url)

            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and not href.startswith('http'):  # Handle relative URLs
                    href = urljoin(url, href)
                if href and href.startswith(url) and href not in visited_urls:
                    extract_path_and_parameters(href)

                    # Recursive call to crawl the website
                    crawl_website(href, user_agent)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


def extract_path_and_parameters(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    parameters = parse_qs(parsed_url.query)
    full_url = urljoin(url, parsed_url.path + "?" + parsed_url.query) if parsed_url.query else url
    print("URL:", full_url)
    print("Path", path)
    print("Parameters", parameters)
    domain = parsed_url.netloc.lstrip("www.")  # Extract the domain and remove "www" prefix
    folder_path = domain  # Specify the path for the folder
    output_file = folder_path + "/directories.txt"  # Specify the path for the directories.txt file

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(output_file, "a") as file:
        file.write(full_url + "\n")
