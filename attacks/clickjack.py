import os
import re
import urllib.request
from pystyle import *


def single_url(url,cors):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0'
    }
    try:
        response = urllib.request.urlopen(url, timeout=5)
        check = response.headers
        with open('temp.txt', 'w') as file:
            file.write(str(check))
        with open('temp.txt', 'r') as file:
            sami = re.findall(r'X-Frame-Options|Content-Security-Policy|x-frame-options|content-security-policy:', file.read())

        if not sami:
            print(Colors.green+f"[ ✔ ] {url} VULNERABLE")
            print(Colors.cyan+f"[+] POC Saved As Vuln.html\n")


            domain = urllib.parse.urlparse(url).netloc.lstrip("www.")  # Extract the domain without the "www" prefix
            folder_path = os.path.join(domain, "results")  # Specify the path for the folder
            output_file = os.path.join(folder_path, "vuln.html")  # Specify the path for the output file
            outi = os.path.join(folder_path, "clickjack.txt")
            with open(outi,'w')as f:
                f.write('''ClickJacking Vulnerability:
The malicious practice of manipulating a website user's activity by concealing hyperlinks beneath legitimate clickable content, thereby causing the user to perform actions of which they are unaware.

Mitigation:
One way to defend against clickjacking is to include a "frame-breaker" script in each page that should not be framed.

Vulnerable URLS:
''')
            with open(outi,'a') as f:
                f.write(f'{url} [VULNERABLE]')
                f.close()
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            with open(cors,'r') as poc_file, open(output_file, 'w') as vuln_file:
                vuln_file.write(poc_file.read().replace('vuln', url))

            os.remove('temp.txt')

        else:
            print(Colors.red+f"[ X ] {url}  NOT VULNERABLE")

    except Exception as e:
        print(Colors.red+f"An error occurred: {e}")

