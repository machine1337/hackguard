import requests
from pystyle import *
def detect_waf(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }

    waf_list = [
        'aeSecure', 'Airlock', 'Akamai', 'AliYunDun', 'Anquanbao', 'Approach', 'Armor', 'AWS WAF', 'Azion', 'Barracuda',
        'BelugaCDN', 'BinarySEC', 'BitNinja', 'BlockDoS', 'Bluedon', 'BulletProof Security', 'CacheFly', 'CDN77',
        'ChinaCache', 'Cloudbric', 'Cloudflare', 'Comodo', 'CrawlProtect', 'DenyALL', 'Distil Networks', 'DoSArrest',
        'DotDefender', 'Edgecast', 'EdgeProtect', 'Eisoo Cloud', 'ExpressionEngine', 'F5 BIG-IP ASM', 'FortiWeb',
        'GoDaddy', 'Greywizard', 'HuaweiCloud', 'HyperGuard', 'Imperva', 'Incapsula', 'IndusGuard', 'Instart Logic',
        'ISA Server', 'Jiasule', 'Kona Site Defender', 'KnownSec', 'LiteSpeed', 'MalCare', 'MaxCDN', 'Mission Control',
        'ModSecurity', 'NAXSI', 'Nemesida', 'NevisProxy', 'Newdefend', 'NinjaFirewall', 'NSFocus', 'Open-Resty Lua Nginx',
        'Oracle', 'Palo Alto Networks', 'PerimeterX', 'PowerCDN', 'Qcloud', 'Reblaze', 'RSFirewall', 'Sabre', 'Safe3WAF',
        'Safedog', 'SecuPress', 'SecureIIS', 'SecureSphere', 'Sitelock', 'ShieldSquare', 'SonicWall', 'Sophos',
        'Sqreen', 'Sucuri', 'Tencent Cloud', 'URLMaster SecurityCheck', 'Varnish', 'Wallarm', 'WatchGuard', 'WebARX',
        'WebKnight', 'West263 CDN', 'Wordfence', 'WTS-WAF', 'Yundun', 'Yunsuo', 'Zenedge', 'zScaler', 'Other WAF'
    ]

    try:
        response = requests.get(url, headers=headers)
        detected_wafs = []
        for waf_name in waf_list:
            if waf_name.lower() in response.headers.get('Server', '').lower():
                detected_wafs.append(waf_name)

        if detected_wafs:
            print(Colors.green+f"[*] WAF DETECTED: {', '.join(detected_wafs)}")
        else:
            print(Colors.red+f"[-] No WAF Detected on {url}")
    except requests.RequestException as e:
        print(Colors.red+f"An error occurred while checking {url}: {str(e)}")

