import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303', headers=headers)

soup=BeautifulSoup(data.text, 'html.parser')

title=soup.select_one('meta[property="og:title"]')['content']
image=soup.select_one('meta[property="og:image"]')['content']
description=soup.select_one('meta[property="og:description"]')['content']

print(title,image,description)

# - soup.select('태그명[속성="값"]')
