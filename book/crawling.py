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

driver = webdriver.Chrome('C:/Users/dmsru/Desktop/shopping/book/chromedriver.exe')
time.sleep(3)

driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')

# 소설 카테고리부터 시작, 1페이지
driver.find_element_by_xpath('//*[@id="memo1"]/div[1]/ul/li[2]').click()
time.sleep(3)

# 펼치기
driver.find_element_by_xpath('//*[@id="memo1"]/div[2]').click()
time.sleep(3)


# 페이지 이동하면서 상세 정보 url 수집
book_page_urls = []
for i in range(1,7) :
    if i != 6:
        nextBtn = driver.find_element_by_xpath(f'//*[@id="section_bestseller"]/div[4]/a[{i}]').click()
    for j in range(0, 25): 
        dl_data = driver.find_element_by_xpath(f'//*[@id="book_title_{j}"]/a').get_attribute("href")
        if dl_data == None :
            break
        time.sleep(3)
        book_page_urls.append(dl_data)
    time.sleep(3)   
    
print('총 개수--->', len(book_page_urls))
# print('url---->',book_page_urls)

# 필요한 정보 수집
def book_data():
    all_book = []
    for index, book_page_url in enumerate(book_page_urls):

        driver.get(book_page_url)
        bsObject = BeautifulSoup(driver.page_source, 'html.parser')

        title = bsObject.find('meta', {'property':'og:title'}).get('content')
        author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
        publisher = bsObject.find('dt', text='출판사').find_next_sibling('dd').text
        
        try :
            price = bsObject.select_one('div.lowest > span.price').text
        except :
            price = bsObject.select_one('div.retail > strong').text

        isbn = bsObject.select('div.book_info_inner > div')[2].text
        if isbn.find('ISBN') == -1 :
            continue
        text_arr = isbn.split(' ')
        result =''
        if text_arr[0] == '\n페이지' :
            if text_arr[3].find('|') != -1 :
                idx = text_arr[3].find('|')
                result = text_arr[3][0:idx]
            else :
                result = text_arr[3]
        elif text_arr[0] == '\nISBN':
            if text_arr[2].find('|') != -1 :
                idx = text_arr[2].find('|')
                result = text_arr[2][0:idx]
            else :
                result = text_arr[2]
            
        image = bsObject.find('meta', {'property':'og:image'}).get('content')
        if bsObject.find('h3', text='목차') == None :
            continue
        section = bsObject.find('h3', text='목차').find_next_sibling('div').text
        # section = section.replace('\n','')
        description = bsObject.find('meta', {'property':'og:description'}).get('content')
        # description = description.replace('\n','')

        title_info = [];author_info = [];publisher_info = [];price_info = [];isbn_info = [];image_info = [];section_info = [];description_info = [];

        title_info.append(title)
        author_info.append(author)
        publisher_info.append(publisher)
        price_info.append(price)
        isbn_info.append(result)
        image_info.append(image)
        section_info.append(section)
        description_info.append(description)

        book_info = [book for book in zip(title_info,author_info,publisher_info,price_info,isbn_info,image_info,section_info,description_info)]
        all_book.append(book_info[0])
                    
    return all_book
