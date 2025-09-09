import requests
import bs4

URL="https://quotes.toscrape.com/page/{}/"
HEADER={'User-Agent': 'Mozilla/5.0'}
NUM=1

while True:
    
    base=requests.get(URL.format(str(NUM)), headers=HEADER,timeout=15)
    base.raise_for_status()
    soup=bs4.BeautifulSoup(base.text,'lxml')
    quote=soup.select('.text')
    author=soup.select('.author')
   

    print(f'------Page{NUM}-----')
    for i in range(min(len(quote), len(author))):
        print(author[i].text)
        print(quote[i].text)
        print()  

    next_button=soup.select('.next')
    if not next_button:
        print("no more pages.")
        break

    NUM+=1
        



