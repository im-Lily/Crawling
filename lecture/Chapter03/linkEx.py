import requests
from bs4 import BeautifulSoup

keyword = input("검색어를 입력하세요: ")
lastPage = int(input("마지막 페이지 번호를 입력해주세요: "))
pageNum = 1
for i in range(1, lastPage*10, 10):
    print(f"{pageNum}페이지입니다. ===================================")
    response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(".news_tit")  # 결과는 리스트
    for link in links:
        title = link.text  # 태그 안의 텍스트 요소를 가져옴
        url = link.attrs['href']  # href 속성값을 가져옴
        print(title, url)
    pageNum = pageNum + 1
