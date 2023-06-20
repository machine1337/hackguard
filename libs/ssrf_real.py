import re
import json
patterns = [

"access=",
"admin=",
"dbg=",
"debug=",
"edit=",
"grant=",
"test=",
"alter=",
"clone=",
"create=",
"delete=",
"disable=",
"enable=",
"exec=",
"execute=",
"load=",
"make=",
"modify=",
"rename=",
"reset=",
"shell=",
"toggle=",
"adm=",
"root=",
"cfg=",
"dest=",
"redirect=",
"uri=",
"path=",
"continue=",
"url=",
"window=",
"next=",
"data=",
"reference=",
"site=",
"html=",
"val=",
"validate=",
"domain=",
"callback=",
"return=",
"page=",
"feed=",
"host=",
"port=",
"to=",
"out=",
"view=",
"dir=",
"show=",
"navigation=",
"open=",
"file=",
"document=",
"folder=",
"pg=",
"php_path=",
"style=",
"doc=",
"img=",
"filename="
]
def ssrf_urls(input_file, ssrf_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Match the patterns against the URLs and save the matching URLs in a file
    with open(ssrf_file, 'w') as file:
        for url in urls:
            if any(pattern in url for pattern in patterns):
                file.write(url)



