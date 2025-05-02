import requests
import time
from fake_useragent import UserAgent

target_url="https://dsdoc.dsone.3ds.com/devdoc/3DEXPERIENCER2018x/en/DSInternalDoc.htm"

req=requests.get(target_url)


with open("extracted_file.html","w", encoding="utf-8") as file:
    file.write(req.text)

