import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for i in range(1, 5):

    page = 'https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200713&hh=01&rtm=N&pg=' + str(i)
    data = requests.get(page, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    Songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

    for song in Songs:
        title = song.select_one('td.info > a.title.ellipsis').text.strip()

        if "19금" in title :
            title = title[3:].strip()

        rank = song.select_one('td[class = "number"]').text[:3].strip()  # 순위만 슬라이싱
        artist = song.select_one('td.info > a.artist.ellipsis').text.strip()
        print(rank, title, "-", artist)
        doc = {
            'rank': rank,
            'title': title,
            'artist': artist
        }
        db.Chart.insert_one(doc)
