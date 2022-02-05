import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

from datetime import datetime
import random

client = MongoClient('localhost', 27017)
board_col = client.flow.board

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rpeople.naver?date=20200128', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select('#old_content > table > tbody > tr')

    urls = []
    for tr in trs:
        a = tr.select_one('td.title > a')
        if a is not None:
            base_url = 'https://movie.naver.com/'
            url = base_url + a['href']
            urls.append(url)

    return urls

# 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.
def insert_star(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    name = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
    title = soup.select_one(
        '#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)').text
    # dd 조심
    # 바로 밑 dd가 생년월일인데 dd > a:nth-child(1) 로하면 생년월일 밑에 a가 없으니까 그 다음 dd를 찾는듯
    contents = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.pf_intro > div').text
    current_utc_time = round(datetime.utcnow().timestamp() * 1000)
    doc = {
        'writer_id': '61f3e3b9369fb61c7814ca42',
        'name': '찬구',
        'title': title,
        'contents': contents,
        "view": random.randrange(30, 777),
        'pubdate': current_utc_time
    }

    board_col.insert_one(doc)
    print('완료!', name)

# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    # boards_col.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        try:
            insert_star(url)
        except:
            pass

### 실행하기
insert_all()
        