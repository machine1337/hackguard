import json
import os
import platform
import re
import socket
import time
import requests
from pystyle import *
banner = Center.XCenter(r"""
*************************************************************************
*     ___   _    _    ____ _  __      ____ _   _   _    ____  ______     *
*    / / | | |  / \  / ___| |/ /     / ___| | | | / \  |  _ \|  _ \ \    *
*   | || |_| | / _ \| |   | ' /_____| |  _| | | |/ _ \ | |_) | | | | |   *
*  < < |  _  |/ ___ \ |___| . \_____| |_| | |_| / ___ \|  _ <| |_| |> >  *
*   | ||_| |_/_/   \_\____|_|\_\     \____|\___/_/   \_\_| \_\____/| |   *
*    \_\                                                          /_/    *
*                    WEB APPLICATION VULNERABILITY SCANNER               *
*                          CODED BY: MACHINE1337                         *
*                                                                        *
**************************************************************************
                            \n\n
""")
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(Colors.green + f"[*] Folder Created Successfully...{folder_path}")
    else:
        print(Colors.red+ "[!] Target Folder Already Exists...")
        print(Colors.red + "[!] Remove Or Replace it...")
        exit()



def write_results_to_file(filename, domain_to_ip, ports, vulns, cpes):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"[ ✔ ] [IP]: {domain_to_ip}\n")
        file.write(f"[ ✔ ] [PORTS]: {ports}\n")
        file.write(f"[ ✔ ] [VULNS]: {vulns}\n")
        file.write(f"[ ✔ ] [INFO]: {cpes}\n")
def fetch_urls_from_wayback(target):
    url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        urls = [entry[0] for entry in data[1:]]
        return urls
    else:
        print(Colors.red+ "[*] Failed To Fetch Urls From Wayback...")
        return []
def detect_http_or_https(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.url
        return 'Unknown'
    except requests.exceptions.RequestException:
        return 'Invalid'
start_time = time.time()
start_time_str = time.ctime(start_time)
def single():
    global single_domain
    global protocol
    single_domain = input(Colorate.Vertical(Colors.green_to_yellow, "[+] Enter Domain Name (site.com): ", 2))
    print(Colorate.Vertical(Colors.green_to_yellow, f"\n[*] Scanning Started on:  {start_time_str}", 2))
    print(Colors.yellow+ "\n[*] Creating Target Folder....")
    folder_path = single_domain
    create_folder_if_not_exists(folder_path)
    checking = single_domain.replace('http://', '').replace('https://', '')
    domain_to_ip = socket.gethostbyname(checking)
    print(Colors.cyan + '\n[-]+++++++++++GETTING TARGET INFORMATION++++++++++++')
    from libs.tech import detect_cms, detect_server
    from libs.waf import detect_waf
    protocol = detect_http_or_https(single_domain)
    url = protocol
    print(Colors.green + f'[-] Target Domain: {checking}')
    print(Colors.green + f'[-] Target IP: {domain_to_ip}')
    print(Colors.green+f'[-] PROTOCOL: {url}')
    cms = detect_cms(single_domain)
    print(Colors.green + f"[-] CMS: {cms}")
    server = detect_server(single_domain)
    print(Colors.green + f"[-] SERVER: {server}")
    detect_waf(url)
    print(Colors.yellow + '\n-----------------------------------------------')
    print(Colors.cyan +'\n[*] Searching For Sensitive Paths & Files.....\n')
    from libs.sensitive import find_sensitive_urls
    find_sensitive_urls(protocol)
    print(Colors.cyan + '\n-----------------------------------------------\n')
    folder_path1 = os.path.join(single_domain, "results")
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)
    from libs.info import scan
    output_file=os.path.join(folder_path1, "Target_info.txt")
    outing=os.path.join(folder_path1, "scanned_ports.txt")
    scan(single_domain, output_file)
    print(Colors.yellow + '\n-----------------------------------------------')
    print(Colors.cyan+"\n[+] Scanning Open Ports And Finding Exploits:-\n")
    dest = f"https://internetdb.shodan.io/{domain_to_ip}"
    response = requests.get(dest)
    data = response.json()
    ports = data.get('ports', [])
    vulns = data.get('vulns', [])
    cpes = data.get('cpes', [])
    print(Colors.cyan+f'[-] Ports: {ports}')
    print(Colors.cyan+f'[-] Vulns: {vulns}')
    print(Colors.cyan+f'[-] Cpes:  {cpes}')
    write_results_to_file(outing, domain_to_ip, ports, vulns, cpes)
    print(Colors.green+f'[-] Results Saved To: {outing}')
    print(Colors.cyan + '\n-----------------------------------------------')
    print(Colors.yellow+'\n[*] Extracting Javascript Urls....\n')
    from libs.javascript import extract_js_links

    js_file = folder_path + '/javascript_urls.txt'
    extract_js_links(url, js_file)
    print(Colors.green+f'[-] Javascript Urls Saved To: {js_file}')
    print(Colors.cyan + '\n-----------------------------------------------')
    print(Colors.yellow+"\n[*] Getting URLS From Public Archives...\n")
    target = single_domain
    wayback_urls = fetch_urls_from_wayback(target)
    unique_urls = set()
    for url in wayback_urls:
        url = url.strip()  # Remove leading/trailing whitespace
        if url:
            unique_urls.add(url)
    filtered_urls = []
    for url in unique_urls:
        if not re.search(r'\.(woff|ttf|svg|eot|png|jpe?g|css|ico)$', url, re.IGNORECASE):
            url = re.sub(r':(80|443)', '', url)
            filtered_urls.append(url)
    output_file = folder_path + '/filtered_urls.txt'  # Path to the output file
    with open(output_file, 'w') as file:
        for url in filtered_urls:
            file.write(url + '\n')
    print(Colors.green+f"[-] Filtered URLs saved to {output_file}")
    time.sleep(1)
    print(Colors.yellow + '\n-----------------------------------------------')
    print(Colors.cyan+"\n[*] Filtering URLS for Open Redirect Vulnerability\n")
    from libs.redirect import apply_sed_filter
    fil_urls = output_file
    red_out = folder_path + '/redirect_urls.txt'
    apply_sed_filter(fil_urls, red_out)
    time.sleep(1)
    print(Colors.green+f"[-] Possible Vulnerable Open Redirect Urls Saved To {red_out}")
    time.sleep(1)
    print(Colors.yellow + '\n-----------------------------------------------\n')
    print(Colors.cyan+"\n[*] Filtering URLS for Cross Site Scripting...")
    from libs.xss_real import apply_sed_filter
    input_file = output_file
    xss_file = folder_path + '/xss_urls.txt'
    apply_sed_filter(input_file, xss_file)
    time.sleep(1)
    print(Colors.green+f'[-] Possible Vulnerable XSS Urls Saved To {xss_file}')
    time.sleep(1)
    print(Colors.yellow + '\n-----------------------------------------------')
    print(Colors.cyan+"\n[*] Filtering URLS for SQL Injection.....\n")
    from libs.sqli_real import sql_urls
    input_file = output_file
    sql_file = folder_path + '/sql_urls.txt'
    sql_urls(input_file, sql_file)
    time.sleep(1)
    print(Colors.green+f"[-] Possible Vulnerable SQLI Urls Saved To {sql_file} ")
    time.sleep(1)
    print(Colors.yellow + '\n-----------------------------------------------')
    print(Colors.cyan+"\n[*] Filtering URLS for Local File Inclusion (LFI)...\n")
    from libs.lfi_real import apply_sed_filter
    fil_urls = output_file
    red_out = folder_path + '/lfi_urls.txt'
    apply_sed_filter(fil_urls, red_out)
    time.sleep(1)
    print(Colors.green+f'[-] Possible Vulnerable LFI Urls Saved To {red_out}')
    attacks()
def attacks():
    folder_path = os.path.join(single_domain, "results")
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print(Colors.cyan + '-----------------------------------------------')
    print(Colors.yellow+"\n[*] Testing For CORS Misconfiguration.........\n")
    from attacks.cors import cors_urls
    url = protocol
    cors_urls(url)
    print(Colors.cyan + '-----------------------------------------------')
    print(Colors.yellow+"[*] Testing For ClickJacking Vulnerability.....\n")
    from attacks.clickjack import single_url
    cors= 'payloads/cors.html'
    single_url(url,cors)
    print(Colors.cyan + '-----------------------------------------------')
    print(Colors.yellow+"[*] Testing For SQL Injection...........")
    from attacks.sql import scan_sql_injection, read_urls_from_file, read_payloads_from_file
    urls_file_path = f'{single_domain}/sql_urls.txt'
    urls = read_urls_from_file(urls_file_path)
    output_file_path = os.path.join(folder_path, "sql_vulnerable_urls.txt")
    payloads_file_path = 'payloads/sql-payloads.txt'  # Specify the path to the file containing the payloads
    payloads = read_payloads_from_file(payloads_file_path)
    scan_sql_injection(urls, payloads,output_file_path)
    print(Colors.cyan + '\n-----------------------------------------------')
    print(Colors.yellow+"\n[*] Testing For Open Redirection vulnerability.....\n")
    from attacks.redirect import red_url
    list_path = f'{single_domain}/redirect_urls.txt'
    payloads_path = 'payloads/redirect-payloads.txt'
    output_path = os.path.join(folder_path, "open-redirect_vulnerable_urls.txt")
    red_url(list_path, payloads_path,output_path)
    print(Colors.cyan + '\n-----------------------------------------------')
    print(Colors.yellow+"\n[*] Searching For LFI vulnerability.........\n")
    from attacks.lfi import detect_lfi_vulnerability
    file_path = f'{single_domain}/lfi_urls.txt'
    payload_list = 'payloads/lfi-payloads.txt'
    output_file = os.path.join(folder_path, "lfi_vulnerable_urls.txt")
    with open(file_path, 'r') as file:
        domains = list(set(file.read().splitlines()))  # Remove duplicates using set()
    all_vulnerable_urls = set()
    for domain in domains:
        detect_lfi_vulnerability(domain, payload_list, all_vulnerable_urls,output_file)
    file_path = output_file
    try:
     with open(file_path, 'r') as file:
         content = file.read()
     url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
     urls = re.findall(url_pattern, content)
     if urls:
        print(Colors.green + f"\n[-] LFI Vulnerable Urls Saved To: {output_file}")
     else:
        print(Colors.red + "[*] NO LFI Vulnerable Urls Found.\n")
    except:
        print(Colors.red + "[*] NO LFI Vulnerable Urls Found.\n")
    ###############################
    print(Colors.cyan + '\n-----------------------------------------------')
    print(Colors.yellow+'\n[*] Testing For XSS Vulnerability........\n')
    from attacks.xss import check_xss_vulnerability
    output_file= os.path.join(folder_path, "xss_vulnerable_urls.txt")
    url_filename= f'{single_domain}/xss_urls.txt'
    payload_filename = 'payloads/xss-payloads.txt'
    check_xss_vulnerability(url_filename, payload_filename,output_file)
    print(Colors.yellow + '\n-----------------------------------------------\n')
    print(Colors.cyan + "\n[*] Bruteforcing Directories.....")
    from libs.dirbs import crawl_website
    website_url = protocol
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0.2 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0.2 Safari/537.36',
    ]
    for user_agent in user_agents:
        crawl_website(website_url, user_agent)
        print()
    elapsed_time = time.time() - start_time
    print(Colors.yellow + '\n-----------------------------------------------\n')
    print(Colorate.Vertical(Colors.yellow_to_red, f"[*] Total Time Taken:  {elapsed_time}", 2))
def menu():
    ans = True
    while ans:
        print(Colors.cyan+"""
      1. START SCAN
      2. SHOW AVAILABLE MODULES
      3. Exit
      """)
        ans = input(Colors.yellow+"[*] Choose From Given Options: ")
        if ans == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
            single()
        elif ans == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
            choose()
        elif ans == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
            print(Colors.red+"\n [+] Thanks For Using HackGuard! See You Tomorrow")
            ans = None
        else:
            print(Colors.red+"\n [+] Not Valid Choice Try again")

def choose():

    print(Colors.yellow+f'''-----------------------------------------------------------------------------------------
1.  WEB DOMAIN INFORMATION(IP, PROTOCOL, CMS DETECTION, SERVER DETECTION, WAF DETECTION) -
2.  SENSITIVE PATH FINDER                                                                -
3.  MISCONFIGURATIONS/SENSITIVE SCANS(WORDPRESS, JOOMLA, DRUPAL, PHPMYADMIN)             -
4.  SCANNING PORTS & LOOKING FOR EXPLOITS                                                -
5.  EXTRACTING JAVASCRIPT URLS                                                           -
6.  GETTING URLS FROM PUBLIC ARCHIVES                                                    -
7.  FILTERNING URLS FOR OPEN REDIRECTION                                                 -
8.  FILTERNING URLS FOR CROSS SITE SCRIPTING                                             -
9.  FILTERNING URLS FOR LOCAL FILE INCLUSION                                             -
10. FILTERNING URLS FOR SQLI INJECTION                                                   -
11. TESTING CORS MISCONFIGURATION                                                        -
12. TESTING CLICKJACKING VULNERABILITY                                                   -
13. TESTING SQLI INJECTION VULNERABILITY                                                 -
14. TESTING OPEN REDIRECT VULNERABILITY                                                  -
15. TESTING LOCAL FILE INCLUSION VULNERABILITY                                           -
16. TESTING CROSS SITE SCRIPTING VULNERABILITY                                           -
17. DIRECTORY BRUTEFORCING                                                               -
------------------------------------------------------------------------------------------
''')

def detect():
    try:
        if platform.system().startswith("Windows"):
            os.system('cls')
            print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
            menu()
        elif platform.system().startswith("Linux"):
            os.system('clear')
            print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
            menu()
    except KeyboardInterrupt:
        print(Colors.red+'\n[!] YOU MESSED WITH THE KEYBOARD.....')

detect()
