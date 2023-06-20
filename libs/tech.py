import socket
from libs.waf import detect_waf
import requests
from pystyle import *
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def detect_cms(domain):
    try:
        # Send a GET request to the domain with custom User-Agent header
        response = requests.get(f"http://{domain}", headers=headers)

        # Extract the response content
        content = response.text

        # Detect CMS based on common patterns
        if "WordPress" in content:
            return "WordPress"
        elif "Joomla" in content:
            return "Joomla"
        elif "Drupal" in content:
            return "Drupal"
        elif "Magento" in content:
            return "Magento"
        else:
            return Colors.red+"NOT DETECTED"

    except requests.exceptions.RequestException as e:
        pass

def detect_server(domain):
    try:
        response = requests.head(f"http://{domain}", headers=headers)
        server = response.headers.get('Server')
        if server:
            return server
        else:
            return Colors.red+"NOT DETECTED"
    except requests.exceptions.RequestException as e:
        pass




