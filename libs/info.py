import requests
import argparse
from pystyle import Colors, Colorate
def get(websiteToScan):
    global user_agent
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }
    return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)

def scan(websiteToScan, output_file):
    if websiteToScan.startswith('http://'):
        proto = 'http://'
        websiteToScan = websiteToScan[7:]
    elif websiteToScan.startswith('https://'):
        proto = 'https://'
        websiteToScan = websiteToScan[8:]
    else:
        proto = 'http://'
    if websiteToScan.endswith('/'):
        websiteToScan = websiteToScan.strip('/')
    websiteToScan = proto + websiteToScan
    print(Colors.yellow + "[*] Checking To See If Site Is Online...")

    try:
        onlineCheck = get(websiteToScan)
    except requests.exceptions.ConnectionError as ex:
        print(Colors.red + f"[*] {websiteToScan} appeas to be Offline...")
    else:
        if onlineCheck.status_code == 200 or onlineCheck.status_code == 301 or onlineCheck.status_code == 302:
            print(Colors.green + f"[*] {websiteToScan} appears to be Online...")
            print(Colors.cyan + "[*] Checking To See If Site Is Redirecting")
            redirectCheck = requests.get(websiteToScan, headers=user_agent)
            if len(redirectCheck.history) > 0:
                if '301' in str(redirectCheck.history[0]) or '302' in str(redirectCheck.history[0]):
                    print(Colors.red+"[!] Site is redirecting to " + redirectCheck.url)
            elif 'meta http-equiv="REFRESH"' in redirectCheck.text:
                print(Colors.red+"[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!")
            else:
                print(Colors.green+"[*] Site does not appear to be redirecting...")
        else:
            print(Colors.red+"[!] " + websiteToScan + " appears to be online but returned a " + str(
                onlineCheck.status_code) + " error.")
            exit()
        print(Colors.yellow+'\n[*] Attempting To Get HTTP HEADERS..........')
        for header in onlineCheck.headers:
            try:
                print(" | " + header + " : " + onlineCheck.headers[header])
            except Exception as ex:
                print(Colors.red+"[!] Error: " + ex.message)

        print(Colors.yellow+'[*] Checking Cpanel........')
        cpanel_url = websiteToScan + '/cpanel'
        try:
            response = requests.head(cpanel_url)
            if response.status_code == 200:
                print(Colors.green+f"[*] cPanel Found: {cpanel_url}\n")

            else:
                print(Colors.red+"[!] cPanel not detected on the website.\n")
        except requests.exceptions.RequestException as e:
            print(Colors.red+"[!] An error occurred:", e)
        print(Colors.yellow + "[+] Running the WordPress scans...")

        wpLoginCheck = requests.get(websiteToScan + '/wp-login.php', headers=user_agent)
        if wpLoginCheck.status_code == 200 and "user_login" in wpLoginCheck.text and "404" not in wpLoginCheck.text:
            print(Colors.green + "[!] Detected: WordPress WP-Login page: " + websiteToScan + '/wp-login.php')
            detection_found = True
        else:
            detection_found = False

        wpAdminCheck = requests.get(websiteToScan + '/wp-admin', headers=user_agent)
        if wpAdminCheck.status_code == 200 and "user_login" in wpAdminCheck.text and "404" not in wpAdminCheck.text:
            print(Colors.green + "[!] Detected: WordPress WP-Admin page: " + websiteToScan + '/wp-admin')
            detection_found = True

        wpAdminUpgradeCheck = get(websiteToScan + '/wp-admin/upgrade.php')
        if wpAdminUpgradeCheck.status_code == 200 and "404" not in wpAdminUpgradeCheck.text:
            print(
                Colors.green + "[!] Detected: WordPress WP-Admin/upgrade.php page: " + websiteToScan + '/wp-admin/upgrade.php')
            detection_found = True

        wpAdminReadMeCheck = get(websiteToScan + '/readme.html')
        if wpAdminReadMeCheck.status_code == 200 and "404" not in wpAdminReadMeCheck.text:
            print(Colors.green + "[!] Detected: WordPress Readme.html: " + websiteToScan + '/readme.html')
            detection_found = True

        wpLinksCheck = get(websiteToScan)
        if 'wp-' in wpLinksCheck.text:
            print(Colors.green + "[!] Detected: WordPress wp- style links detected on index")
            detection_found = True

        if not detection_found:
            print(Colors.red + "[!] No Wordpress Misconfiguration Found!!!")

        ####################################################
        # Joomla Scans
        ####################################################

        print(Colors.yellow + "\n[+] Running the Joomla scans...")

        joomlaAdminCheck = get(websiteToScan + '/administrator/')
        if joomlaAdminCheck.status_code == 200 and "mod-login-username" in joomlaAdminCheck.text and "404" not in joomlaAdminCheck.text:
            print(
                Colors.green + "[!] Detected: Potential Joomla administrator login page: " + websiteToScan + '/administrator/')
            detection_found = True
        else:
            detection_found = False

        joomlaReadMeCheck = get(websiteToScan + '/readme.txt')
        if joomlaReadMeCheck.status_code == 200 and "joomla" in joomlaReadMeCheck.text and "404" not in joomlaReadMeCheck.text:
            print(Colors.green + "[!] Detected: Joomla Readme.txt: " + websiteToScan + '/readme.txt')
            detection_found = True

        joomlaTagCheck = get(websiteToScan)
        if joomlaTagCheck.status_code == 200 and 'name="generator" content="Joomla' in joomlaTagCheck.text and "404" not in joomlaTagCheck.text:
            print(Colors.green + "[!] Detected: Generated by Joomla tag on index")
            detection_found = True

        joomlaStringCheck = get(websiteToScan)
        if joomlaStringCheck.status_code == 200 and "joomla" in joomlaStringCheck.text and "404" not in joomlaStringCheck.text:
            print(Colors.green + "[!] Detected: Joomla strings on index")
            detection_found = True

        joomlaDirCheck = get(websiteToScan + '/media/com_joomlaupdate/')
        if joomlaDirCheck.status_code == 403 and "404" not in joomlaDirCheck.text:
            print(
                Colors.green + "[!] Detected: Joomla media/com_joomlaupdate directories: " + websiteToScan + '/media/com_joomlaupdate/')
            detection_found = True

        if not detection_found:
            print(Colors.red + "[!] No Joomla Misconfiguration Found!!!")

        ####################################################
        # Drupal Scans
        ####################################################
        print(Colors.yellow + "\n[+] Running the Drupal scans...")

        drupalReadMeCheck = get(websiteToScan + '/readme.txt')
        if drupalReadMeCheck.status_code == 200 and 'drupal' in drupalReadMeCheck.text and '404' not in drupalReadMeCheck.text:
            print(Colors.green + "[!] Detected: Drupal Readme.txt: " + websiteToScan + '/readme.txt')
            detection_found = True

        drupalTagCheck = get(websiteToScan)
        if drupalTagCheck.status_code == 200 and 'name="Generator" content="Drupal' in drupalTagCheck.text:
            print(Colors.green + "[!] Detected: Generated by Drupal tag on index")
            detection_found = True

        drupalCopyrightCheck = get(websiteToScan + '/core/COPYRIGHT.txt')
        if drupalCopyrightCheck.status_code == 200 and 'Drupal' in drupalCopyrightCheck.text and '404' not in drupalCopyrightCheck.text:
            print(Colors.green + "[!] Detected: Drupal COPYRIGHT.txt: " + websiteToScan + '/core/COPYRIGHT.txt')
            detection_found = True

        drupalReadme2Check = get(websiteToScan + '/modules/README.txt')
        if drupalReadme2Check.status_code == 200 and 'drupal' in drupalReadme2Check.text and '404' not in drupalReadme2Check.text:
            print(Colors.green + "[!] Detected: Drupal modules/README.txt: " + websiteToScan + '/modules/README.txt')
            detection_found = True

        drupalStringCheck = get(websiteToScan)
        if drupalStringCheck.status_code == 200 and 'drupal' in drupalStringCheck.text:
            print(Colors.green + "[!] Detected: Drupal strings on index")
            detection_found = True

        if not detection_found:
            print(Colors.red + "[!] No Drupal Misconfiguration Found!!!")

        ####################################################
        # phpMyAdmin Scans
        ####################################################

        print(Colors.yellow + "\n[+] Running the phpMyAdmin scans...")

        phpMyAdminCheck = get(websiteToScan)
        if phpMyAdminCheck.status_code == 200 and 'phpmyadmin' in phpMyAdminCheck.text:
            print(Colors.green + "[!] Detected: phpMyAdmin index page")
            detection_found = True

        pmaCheck = get(websiteToScan)
        if pmaCheck.status_code == 200 and ('pmahomme' in pmaCheck.text or 'pma_' in pmaCheck.text):
            print(Colors.green + "[!] Detected: phpMyAdmin pmahomme and pma_ style links on index page")
            detection_found = True

        phpMyAdminConfigCheck = get(websiteToScan + '/config.inc.php')
        if phpMyAdminConfigCheck.status_code == 200 and '404' not in phpMyAdminConfigCheck.text:
            print(Colors.green + "[!] Detected: phpMyAdmin configuration file: " + websiteToScan + '/config.inc.php')
            detection_found = True

        if not detection_found:
            print(Colors.red + "[!] No PHPMYADMIN Misconfiguration Detected!!!")


