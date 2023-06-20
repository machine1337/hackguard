import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from tqdm import tqdm
from pystyle import *
s = requests.Session()
s.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"


def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = {line.strip() for line in file if line.strip()}  # Use a set instead of a list
    return urls


def read_payloads_from_file(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file if line.strip()]
    return payloads


def save_vulnerable_urls(file_path, vulnerabilities):
    with open(file_path,'w') as f:
        f.write('''SQL INJECTION:
SQL injection is a code injection technique that might destroy your database. SQL injection is one of the most common web hacking techniques.

Mitigation:
The only sure way to prevent SQL Injection attacks is input validation and parametrized queries including prepared statements.

Vulnerable URLS:
''')
    with open(file_path, 'a') as file:
        for url in vulnerabilities:
            file.write(url + '\n')


def scan_sql_injection(urls, payloads, output_file_path):
    progress_bar = tqdm(total=len(urls) * len(payloads), desc="Scanning")
    vulnerabilities = set()  # Use a set to store vulnerabilities

    for url in urls:
        for payload in payloads:
            new_url = f"{url}{payload}"
            res = s.get(new_url)
            progress_bar.update(1)
            if is_vulnerable(res):
                vulnerabilities.add(new_url)  # Add vulnerable URL to the set
                break  # Stop applying other payloads on the same URL

    progress_bar.close()

    if vulnerabilities:
        print(Colors.cyan+"[+] SQL Injection vulnerabilities found:")
        for url in vulnerabilities:
            print(Colors.green+"SQL FOUND: -", url)
        save_vulnerable_urls(output_file_path, vulnerabilities)
    else:
        print(Colors.red+"\n[-] No SQL Injection vulnerabilities detected.\n")
