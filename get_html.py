import requests
import time
from fake_useragent import UserAgent

target_url="some_url"

req=requests.get(target_url)


with open("extracted_file.html","w", encoding="utf-8") as file:
    file.write(req.text)

