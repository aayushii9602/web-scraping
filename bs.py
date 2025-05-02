from bs4 import BeautifulSoup

with open("extracted_file.html", "r", encoding="utf-8") as f:
    html = f.read() 

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())
print(soup.title.text)

links=soup.find_all('a')
print(soup.a)
text=soup.get_text()

with open("extracted_text.txt","w", encoding="utf-8") as file:
    file.write(text)
