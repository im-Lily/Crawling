import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dbInsert import insert_review_data

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 파라미터
city = 14690  # 서울
checkIn = "2023-04-03"
checkOut = "2023-04-07"

# 웹페이지 해당 주소 이동
# driver.get("https://www.goodchoice.kr/product/search/2")
driver.get("https://www.goodchoice.kr/product/search/2/2014")

# 로딩이 끝날 때까지 5초 기다리기
driver.implicitly_wait(5)

# 호텔 클릭
hotel = driver.find_element(By.CLASS_NAME, "stage.gra_black_vertical")
hotel.click()

# 리뷰 클릭
reviewButton = driver.find_element(By.CLASS_NAME, "tab_review")
reviewButton.click()

title_list = []
rating_list = []
name_list = []
content_list = []
imgUrl_list = []

review_data = {}
# 전체 리뷰
def get_review():
    for i in range(1, 16):
        title = driver.find_element(By.CSS_SELECTOR, f"#review > ul > li:nth-child({i}) > div > strong").text
        rating = driver.find_element(By.CSS_SELECTOR,
                                     f"#review > ul > li:nth-child({i}) > div > div.score_wrap_sm > div.num").text
        before_name = driver.find_element(By.CSS_SELECTOR,
                                          f"#review > ul > li:nth-child({i}) > div > div.name > b").text
        name = re.sub('·', '', before_name)
        before_content = driver.find_element(By.CSS_SELECTOR,
                                             f"#review > ul > li:nth-child({i}) > div > div.txt").text
        content = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                         '', before_content)
        content = re.sub("\n", " ", content)
        try:
            imgUrl = driver.find_element(By.XPATH,
                                         f'//*[@id="review"]/ul/li[{i}]/div/div[4]/div/ul/li/img').get_attribute(
                "src")
        except Exception as e:
            imgUrl = ""
            pass

        review_data['title'] = title
        review_data['rating'] = rating
        review_data['content'] = content
        review_data['imgUrl'] = imgUrl

        # insert_review_data(review_data)

        title_list.append(title)
        rating_list.append(rating)
        name_list.append(name)
        content_list.append(content)
        imgUrl_list.append(imgUrl)

    # 크롤링 결과 엑셀 파일로 저장
    data = {"title": title_list, "rating": rating_list, "name": name_list, "content": content_list,
            "imgUrl": imgUrl_list}
    df = pd.DataFrame(data)
    df.to_csv('호텔 리뷰 데이터.csv', encoding='utf-8')

    driver.close()


def main():
    get_review()


if __name__ == "__main__":
    main()
