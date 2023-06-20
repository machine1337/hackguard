import os
from urllib.parse import urlparse

import requests
from pystyle import *


def cors_urls(url):
    headers = {
        'Origin': 'example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.options(url, headers=headers, timeout=5)
        response_text = response.text

        domain = urlparse(url).netloc.lstrip("www.")  # Extract the domain without the "www" prefix
        folder_path = os.path.join(domain, "results")  # Specify the path for the folder
        output_file = os.path.join(folder_path, "cor_vuln.txt")  # Specify the path for the output file

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if 'example' in response_text:
            print(Colors.green + f"[-] URL: {url}  [Vulnerable]\n")
            with open(output_file,'w') as f:
                f.write('''CORS MISCONFIGURATION:
A cross-origin resource-sharing misconfiguration occurs when the web server allows third-party domains to perform privileged tasks through the browsers of legitimate users. As the CORS mechanism relies on HTTP headers, a browser makes preflight requests to the cross-domain resource and checks whether the browser will be authorized to serve the actual request. Therefore, improper configuration of CORS headers allows malicious domains to access and exploit the web server’s API endpoints.

Mitigation:
Some best practices to prevent CORS attacks include: Enforcing authentication on resources that have the Access-Control-Allow-Credentials configuration set to true. Use a whitelist for the Access-Control-Allow-Origin header instead of a wildcard.

VULNERABLE URLS:
''')
            with open(output_file, 'a') as f:
                f.write(f"URL: {url} [Vulnerable]")

        else:
            print(Colors.cyan + f"URL: {url}  [Not Vulnerable]\n")

    except requests.exceptions.RequestException as e:
        print(Colors.red + f"[-] An error occurred for URL: {url}\n")



