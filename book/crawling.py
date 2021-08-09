import pymysql
# from pymysql import cursors
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
book_page_urls = []
for index in range(0, 25):
    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)


# 메타 정보와 본문에서 필요한 정보를 추출합니다.
for index, book_page_url in enumerate(book_page_urls):

    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')


    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    image = bsObject.find('meta', {'property':'og:image'}).get('content')
    url = bsObject.find('meta', {'property':'og:url'}).get('content')

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

    book_info = [book for book in zip(title_info, author_info, image_info, url_info, price_info)]

    print(book_info)

    host_name = "shop-book.ciclmc7wjq3o.ap-northeast-2.rds.amazonaws.com"
    user_name = "shopmaster"
    password = "springbook11"
    database_name = "shop_book"

    db = pymysql.connect(
        host=host_name,
        port=3306,
        user=user_name,
        passwd=password,
        db=database_name,
        charset="utf8"
    )

    cursor = db.cursor()
    cursor.execute("set names utf8")
    db.commit()


    for book in book_info:  
        print(book)
        sql = "INSERT INTO Book (book_nm, writer, thumbnail_url, book_info_url, price) VALUES (%s, %s, %s, %s, %s)"
        val = book
        cursor.execute(sql, val)

    # i = 1 
    # for book in book_info: 
    #     cursor.execute( 
    #         f"INSERT INTO Book VALUES({i},\"{book[0]}\",\"{book[1]}\",\"{book[2]}\",\"{book[3]}\",\"{book[4]}\")") 
    #     i += 1

    db.commit()
    db.close()


