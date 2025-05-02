from requests_html import HTMLSession

session=HTMLSession()

target_url="some_url"
r=session.get(target_url)

print(r.text)
# print(r.html.links)