import re
import json
patterns= [

         "id=",
        "select=",
        "report=",
        "role=",
        "update=",
        "query=",
        "user=",
        "name=",
        "sort=",
        "where=",
        "search=",
        "params=",
        "process=",
        "row=",
        "view=",
        "table=",
        "from=",
        "sel=",
        "results=",
        "sleep=",
        "fetch=",
        "order=",
        "keyword=",
        "column=",
        "field=",
        "delete=",
        "string=",
        "number=",
        "filter="
]
def sql_urls(input_file, sql_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    # Match the patterns against the URLs and save the matching URLs in a file
    with open(sql_file, 'w') as file:
        for url in urls:
            if any(pattern in url for pattern in patterns):
                file.write(url)

