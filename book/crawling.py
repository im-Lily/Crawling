from datetime import time
import pymysql
import sys
import os
import rds_auth
import insertDB
import logging
import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = "https://book.naver.com/bestsell/bestseller_list.nhn"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(3)

driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')


# 카테고리 이동(2,29)
def cateBtn() :
    for i in range(2,4) :
        cate = driver.find_element_by_xpath(f'//*[@id="memo1"]/div[1]/ul/li[{i}]').click()
        time.sleep(2)
        pageBtn()
    return cate

def pageBtn() :
    # 페이지 이동(1,6)
    for i in range(1,3) :
        nextBtn = driver.find_element_by_xpath(f'//*[@id="section_bestseller"]/div[4]/a[{i}]').click()
        time.sleep(2)   
    return nextBtn


# 상세 페이지(0,25)
book_page_urls = []
for index in range(0, 3):
    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)
print('url---->',book_page_urls)


# 메타 정보와 본문에서 필요한 정보를 추출합니다.
# def book_data():
all_book = []
for index, book_page_url in enumerate(book_page_urls):

    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')

    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    publisher = bsObject.find('dt', text='출판사').find_next_sibling('dd').text
    dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]
    price = dd.select('div.lowest span.price')[0].text
    # isbn_tag = '#isbnBtn'
    # isbn = bsObject.select(isbn_tag)
    # print("isbn 제발!!", isbn)
    
    image = bsObject.find('meta', {'property':'og:image'}).get('content')
    section = bsObject.find('h3', text='목차').find_next_sibling('div').text
    section = re.sub('\n\n','',section)
    description = bsObject.find('meta', {'property':'og:description'}).get('content')
    description = description.replace('\n',"")
    
    title_info = [];author_info = [];publisher_info = [];price_info = [];image_info = [];section_info = [];description_info = [];

    title_info.append(title)
    author_info.append(author)
    publisher_info.append(publisher)
    price_info.append(price)
    image_info.append(image)
    section_info.append(section)
    description_info.append(description)
     
    book_info = [book for book in zip(title_info,author_info,publisher_info,price_info,image_info,section_info,description_info)]
    all_book.append(book_info[0])

    print('all--->',all_book)    





