from requests_html import HTMLSession

session=HTMLSession()

target_url="https://dsdoc.dsone.3ds.com/devdoc/3DEXPERIENCER2018x/en/DSInternalDoc.htm"
r=session.get(target_url)

print(r.text)
# print(r.html.links)