import re
import json
patterns = [
    "q=",
    "s=",
    "search=",
    "lang=",
    "keyword=",
    "query=",
    "page=",
    "keywords=",
    "year=",
    "view=",
    "email=",
    "type=",
    "name=",
    "p=",
    "callback=",
    "jsonp=",
    "api_key=",
    "api=",
    "password=",
    "email=",
    "emailto=",
    "token=",
    "username=",
    "csrf_token=",
    "unsubscribe_token=",
    "id=",
    "item=",
    "page_id=",
    "month=",
    "immagine=",
    "list_type=",
    "url=",
    "terms=",
    "categoryid=",
    "key=",
    "l=",
    "begindate=",
    "enddate="
]

def apply_sed_filter(fil_urls, red_out):
    # Read the file containing URLs
    with open(fil_urls, 'r') as file:
        urls = file.readlines()

    # Apply the sed filter and save the result in a file
    with open(red_out, 'w') as file:
        for url in urls:
            if any(pattern in url for pattern in patterns):
                modified_url = re.sub(r'=\S*', '=', url)
                file.write(modified_url)