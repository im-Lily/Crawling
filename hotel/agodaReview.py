import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import ActionChains as ac
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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
driver.get(
    f"https://www.agoda.com/ko-kr/search?city={city}&checkIn={checkIn}&los=7&rooms=1&adults=2&children=0&cid=1891463&locale=ko-kr&ckuid=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&prid=0&gclid=Cj0KCQiAo-yfBhD_ARIsANr56g4pwcsS19tYA-Q-W-BkS6FRQeDI_evgrc29NpSYRF9_uIF60NZXHI4aAi2oEALw_wcB&currency=KRW&correlationId=4397fe57-a697-4c3a-b922-f0d231cc77d6&analyticsSessionId=1862650282257724021&pageTypeId=1&realLanguageId=9&languageId=9&origin=KR&tag=45b17d1d-e0b0-fe2a-ce90-5513829d856b&userId=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=sg-pc-6g-acm-web-user-848947997-z64n8&trafficGroupId=5&sessionId=ogfkq2xyxreye2g4q04mgvxs&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&checkOut={checkOut}&priceCur=KRW&textToSearch=%EC%84%9C%EC%9A%B8&travellerType=1&familyMode=off&productType=-1")

# 로딩이 끝날 때까지 5초 기다리기
driver.implicitly_wait(5)

html = driver.page_source
soup = bs(html, 'html.parser')

# 호텔 클릭
hotelName = driver.find_element(By.CLASS_NAME, "sc-iBPRYJ.sc-fubCfw.dyNXNh.gUwDYQ")
hotelName.click()

# TODO
# 리뷰 영역까지 스크롤
scroll_point = driver.find_element(By.ID, 'reviewFilterSection')
ac(driver).move_to_element(scroll_point).perform()

html = driver.page_source
soup = bs(html, 'html.parser')



button = driver.find_element(By.XPATH, '//*[@id="reviewFilterSection"]/div[3]/div[1]')

ac(driver).move_to_element(button).click().perform
time.sleep(2)
button = driver.find_element(By.XPATH, '//*[@id="reviewFilterSection"]/div[3]/div[1]')
ac(driver).move_to_element(button).click().perform
time.sleep(2)
button = driver.find_element(By.XPATH, '//*[@id="reviewFilterSection"]/div[1]/div[3]')
ac(driver).move_to_element(button).click().perform()
time.sleep(2)

# 한국어클릭
button = driver.find_element(By.XPATH, '//*[@id="reviewFilterSection"]/div[1]/div[3]/div/ul/li[2]')
ac(driver).move_to_element(button).click().perform()
time.sleep(2)

driver.implicitly_wait(5)

# 다시 파싱
html = driver.page_source
soup = bs(html, 'html.parser')

### 리뷰 가져오기
# 총 리뷰 개수 찾기 : for문을 몇 번 돌릴지 구하기위함 (버튼을 몇 번 눌러야 할지)
html = driver.page_source
soup = bs(html, 'html.parser')
review_sum0 = soup.select('.Review__FilterContainer__Dropbox > span')  # 이게 아니었네용
review_sum0 = review_sum0[0].text.split("(")[1][:-1]

# 실제 이용후기 개수
review_sum = soup.select('span.Review__SummaryContainer--left.Review__SummaryContainer__Text')[0].text
review_sum = review_sum.split(" ")[3][:-1]

pages = int(review_sum)

# 데이터프레임으로 만들 딕셔너리 정의
reviews = {'score': [], 'text': []}

# page 넘어가기
for k in range(1, pages + 1):
    html = driver.page_source
    soup = bs(html, 'html.parser')

    # 리뷰 영역까지 스크롤
    scroll_point = driver.find_element(By.ID, 'review-0')
    ac(driver).move_to_element(scroll_point).perform()

    # 다시 파싱
    html = driver.page_source
    soup = bs(html, 'html.parser')

    for k in range(0, 9):
        date_ = soup.select(
            f'#review-{k} > div.Review-comment-right > div.Review-comment-bubble > div.Review-statusBar > div > div > span')

        year = date_[0].text.split(" ")[1][:-1]
        if int(year) >= 2018:
            score = soup.select(
                f'#review-{k} > div.Review-comment-left > div > div.Review-comment-leftHeader > div.Review-comment-leftScore')
            text = soup.select(
                f'#review-{k} > div.Review-comment-right > div.Review-comment-bubble > div.Review-comment-body > p.Review-comment-bodyText')

            reviews['score'].append(score[0].text)
            reviews['text'].append(text[0].text)
        else:
            break

    # 버튼누르기
    button = driver.find_element(By.XPATH, '//*[@id="reviewSection"]/div[4]/div/span[3]')
    ac(driver).move_to_element(button).click().perform()
    time.sleep(2)

# 호텔명
hotel = soup.select('.HeaderCerebrum__Name')
hotel

# 호텔명
reviews['title'] = hotel[0].text
reviews
