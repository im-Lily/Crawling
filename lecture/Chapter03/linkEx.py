import requests
from bs4 import BeautifulSoup

response = requests.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%98%AC%EB%A6%AC%EB%B8%8C%EC%98%81")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
links = soup.select(".news_tit") # 결과는 리스트
for link in links:
    title = link.text # 태그 안의 텍스트 요소를 가져옴
    url = link.attrs['href'] # href 속성값을 가져옴
    print(title, url)
