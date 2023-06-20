import requests
from tqdm import tqdm
from pystyle import *

def red_url(list_path, payloads_path, output_path):
    with open(list_path, 'r') as url_file:
        urls = list(set(url_file.read().splitlines()))  # Remove duplicates using set and convert back to a list

    with open(payloads_path, 'r') as payload_file:
        payloads = payload_file.read().splitlines()

    vulnerable_urls = set()  # Set to store vulnerable URLs

    with tqdm(urls, desc="Progress") as pbar:
        for url in pbar:
            is_vulnerable = False  # Flag variable to track vulnerability for the URL
            for payload in payloads:
                full_url = url + payload
                try:
                    response = requests.head(full_url, timeout=5)
                    if response.status_code == 302:
                        with open(f'{output_path}','w') as vuln_file:
                            vuln_file.write('''Open Redirect vulnerability:
An open redirect vulnerability occurs when an application allows a user to control a redirect or forward to another URL. If the app does not validate untrusted user input, an attacker could supply a URL that redirects an unsuspecting victim from a legitimate domain to an attacker's phishing site.

Mitigation:
* Simply avoid using redirects and forwards.
* If used, do not allow the URL as user input for the destination.
* Where possible, have the user provide short name, ID or token which is mapped server-side to a full target URL.

Vulnerable URLS:
''')
                        with open(f'{output_path}', 'a') as vuln_file:
                            vuln_file.write(f"URL: {full_url} [Payload: {payload}]\n")
                        vulnerable_urls.add((url, payload))  # Add URL and payload as a tuple to the set
                        is_vulnerable = True  # Set the flag to True
                        break
                except requests.exceptions.RequestException:
                    pass

            pbar.set_postfix(vulnerable=len(vulnerable_urls))

            if is_vulnerable:
                continue  # Skip applying other payloads for this URL

    if vulnerable_urls:
        print(Colors.cyan + "[-] Open Redirect Vulnerable URLs Found:\n")
        for url, payload in vulnerable_urls:
            print(Colors.green + f"URL: {url} [Payload: {payload}]")
    else:
        print(Colors.red + "\n[*] No Open Redirect vulnerable URLs found\n")
