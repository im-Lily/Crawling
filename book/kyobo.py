from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(3)


driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')


# 1. 페이지 리스트
page_list = []
paging = bsObject.select_one('div.list_paging')
pages = paging.select('ul > li > a')
for page in pages:
    page_list.append(page.get('href'))


# 2. 상세 페이지 리스트
book_page_urls = []
for cover in bsObject.find_all('div', {'class':'detail'}):
    link = cover.select('a')[0].get('href')
    book_page_urls.append(link)


# 3. 데이터 가져오기
all_book = []
def book_data():
    for index, book_page_url in enumerate(book_page_urls):
        
        driver.get(book_page_url)
        bsObject = BeautifulSoup(driver.page_source, 'html.parser')
        
        title = bsObject.find('meta', {'property':'og:title'}).get('content')
        title = re.sub('- 교보문고','',title)
        author = bsObject.find('meta', {'property':'og:author'}).get('content')
        publisher = bsObject.find('span',{'title':'출판사'}).text
        publisher = re.sub('\n','',publisher)
        price = bsObject.find('meta', {'property':'og:price'}).get('content')
        isbn = bsObject.find('span', {'title':'ISBN-13'}).text
        image = bsObject.find('meta', {'property':'og:image'}).get('content')
        description = bsObject.find('meta', {'property':'og:description'}).get('content')
        section = bsObject.find('div',{'class':'box_detail_article'}).text
        section = section.replace('\t','').replace('\n','')

        title_info = [];author_info = [];publisher_info = [];price_info = [];isbn_info = [];image_info = [];description_info = [];section_info = []

        title_info.append(title)
        author_info.append(author)
        publisher_info.append(publisher)
        price_info.append(price)
        isbn_info.append(isbn)
        image_info.append(image)
        description_info.append(description)
        section_info.append(section)      

        book_info = [book for book in zip(title_info,author_info,publisher_info,price_info,isbn_info,image_info,description_info,section_info)]
        all_book.append(book_info[0])

    driver.close()

    return all_book
        

    


        

