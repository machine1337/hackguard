import re

# Define the patterns to match against
patterns = [
    "Lmage_url=",
    "Open=",
    "callback=",
    "cgi-bin/redirect.cgi",
    "cgi-bin/redirect.cgi?",
    "checkout=",
    "checkout_url=",
    "continue=",
    "data=",
    "dest=",
    "destination=",
    "dir=",
    "domain=",
    "feed=",
    "file=",
    "file_name=",
    "file_url=",
    "folder=",
    "folder_url=",
    "forward=",
    "from_url=",
    "go=",
    "goto=",
    "host=",
    "html=",
    "image_url=",
    "img_url=",
    "load_file=",
    "load_url=",
    "login?to=",
    "login_url=",
    "logout=",
    "navigation=",
    "next=",
    "next_page=",
    "out=",
    "page=",
    "page_url=",
    "path=",
    "port=",
    "redir=",
    "redirect=",
    "redirect_to=",
    "redirect_uri=",
    "redirect_url=",
    "reference=",
    "return=",
    "returnTo=",
    "return_path=",
    "return_to=",
    "return_url=",
    "rt=",
    "rurl=",
    "show=",
    "site=",
    "target=",
    "to=",
    "uri=",
    "url=",
    "val=",
    "validate=",
    "view=",
    "window="
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


