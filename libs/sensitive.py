import requests
import concurrent.futures
from pystyle import *
def check_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(Colors.green+f"[-] Sensitive URL found: {url}")

def find_sensitive_urls(party):
    # Add common sensitive paths to check
    sensitive_paths = ['/cpanel', '/admin', '/login', '/wp-admin', '/admin.php', '/wp-login.php',
                       '/administrator', '/moderator', '/manager', '/user', '/admin_login',
                       '/adminpanel', '/superadmin', '/sysadmin', '/signin', '/log_in', '/auth',
                       '/controlpanel', '/login.php', '/admin/index.php', '/user/login',
                       '/secure', '/members', '/webmaster', '/root', '/account', '/admin_area',
                       '/admin_login.php', '/adminpanel.php', '/adm.php', '/admincontrol.php',
                       '/admincp', '/admcp', '/admin_login.asp', '/adminpanel.asp', '/adm.asp',
                       '/admincontrol.asp', '/admincp.asp', '/adm/admloginuser.asp', '/admin2.asp',
                       '/admincontrol/login.asp', '/admin/admin-login.asp',
                       '/config.ini', '/config.php', '/config.php.bak', '/config.inc', '/config.backup',
                       '/config.txt', '/backup', '/backups', '/backup.zip', '/backup.tar.gz', '/backup.tgz',
                       '/.git', '/.git/config', '/.gitignore']

    urls = [f"{party}{path}" for path in sensitive_paths]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_url, urls)


