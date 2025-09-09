import requests
import bs4

URL='https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en'
HEADERS = {"User-Agent": "Mozilla/5.0"}

result=requests.get(URL, headers=HEADERS,timeout=15)
soup=bs4.BeautifulSoup(result.text,'lxml')

