import os

import requests
from tqdm import tqdm
from pystyle import *


def detect_lfi_vulnerability(domain, payload_list, vulnerable_urls,output_file):
    set()
    with open(payload_list, 'r') as file:
        payloads = file.read().splitlines()

    with requests.Session() as session:
        total_iterations = len(payloads)
        progress_desc = f"Scanning Urls: 0%"
        progress_bar = tqdm(total=total_iterations, bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}',
                            leave=False, ncols=0, desc=progress_desc)

        for payload in payloads:
            url = domain + payload
            try:
                response = session.get(url, timeout=5)
                file_content = response.text
            except requests.exceptions.RequestException:
                continue
            if 'root:x' in file_content:
                if url not in vulnerable_urls:
                    vulnerable_urls.add(url)

            progress_bar.update(1)

        progress_bar.set_description("100%")
        progress_bar.close()

    if len(vulnerable_urls) > 0:

        for url in vulnerable_urls:
            print(Colors.green+f'\nVulnerable: {url}\n')
        with open(output_file,'w') as f:
            f.write('''Local File Inclusion:
Local file inclusion (also known as LFI) is the process of including files, that are already locally present on the server, through the exploiting of vulnerable inclusion procedures implemented in the application

Mitigation:
* If possible, do not permit file paths to be appended directly. Make them hard-coded or selectable from a limited hard-coded path list via an index variable.
* It's important to limit the API to allow inclusion only from a directory and directories below it. This ensures that any potential attack cannot perform a directory traversal attack.

Vulnerable URLS:
''')
        with open(output_file, 'a') as output:
            for url in vulnerable_urls:
                output.write(url + '\n')
