import pymysql
import sys
import os
import rds_auth
import insertDB
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = "https://book.naver.com/bestsell/bestseller_list.nhn"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)


# 네이버의 베스트셀러 웹페이지를 가져옵니다.
driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')


# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
# cur_page = 1
# end_page = 5
# while cur_page <= end_page :
book_page_urls = []
for index in range(0, 25):
    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)
    # driver.back()
    # cur_page += 1


# 메타 정보와 본문에서 필요한 정보를 추출합니다.
def book_data():
    all_book = []
    for index, book_page_url in enumerate(book_page_urls):

        driver.get(book_page_url)
        bsObject = BeautifulSoup(driver.page_source, 'html.parser')

        title = bsObject.find('meta', {'property':'og:title'}).get('content')
        author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
        publisher = bsObject.find('dt', text='출판사').find_next_sibling('dd').text
        # ISBN = bsObject.find('div', {'class':'book_info_inner'}).find_next_sibling('em')
        # ISBN = bsObject.find('em', text='페이지').text
        image = bsObject.find('meta', {'property':'og:image'}).get('content')
        url = bsObject.find('meta', {'property':'og:url'}).get('content')
        description = bsObject.find('meta', {'property':'og:description'}).get('content')
        section = bsObject.find('h3', text='목차').find_next_sibling('div').text

        # print("ISBN : ", ISBN)

        dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]
        Price = dd.select('div.lowest span.price')[0].text

        title_info = []
        author_info = []
        image_info = []
        url_info = []
        price_info = []

        title_info.append(title)
        author_info.append(author)
        image_info.append(image)
        url_info.append(url)
        price_info.append(Price)

        book_info = [book for book in zip(title_info, author_info,image_info, url_info, price_info)]
        all_book.append(book_info[0])

    return all_book

book_data()







