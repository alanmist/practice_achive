import requests
import bs4
result=requests.get("https://quotes.toscrape.com/")

soup=bs4.BeautifulSoup(result.text,"lxml")

quote=soup.select('.text')
author=soup.select('.author')

for i in range(min(len(quote), len(author))):
    print(author[i].text)
    print(quote[i].text)
    print() 
