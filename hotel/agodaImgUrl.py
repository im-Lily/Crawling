import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dbConnection import save_main_data, save_detail_data

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
    f"https://www.agoda.com/ko-kr/search?city={city}&checkIn={checkIn}&los=7&rooms=1&adults=2&children=0&cid=1891463&locale=ko-kr&ckuid=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&prid=0&gclid=Cj0KCQiArsefBhCbARIsAP98hXRDutveTPNpWIfQLXDpoMElaN4JKjVtcEroqVIe_mgLos7C4swF9hAaAv3HEALw_wcB&currency=KRW&correlationId=60839d4e-ec58-4c59-937b-3f3710949d9c&analyticsSessionId=-7982247166164195812&pageTypeId=1&realLanguageId=9&languageId=9&origin=KR&tag=45b17d1d-e0b0-fe2a-ce90-5513829d856b&userId=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=hk-pc-2g-acm-web-user-cfc54bf5c-pw9vs&trafficGroupId=5&sessionId=15r2ueyomnlsg0dnubz31jmi&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&checkOut={checkOut}&priceCur=KRW&textToSearch=%EC%84%9C%EC%9A%B8&productType=-1&travellerType=1&familyMode=off")

# 로딩이 끝날 때까지 5초 기다리기
driver.implicitly_wait(5)

img_url_info = {}

# 이미지 url 가져오는 함수
def get_img_url(driver):
    # 숙소 외관 이미지
    mainImgList = driver.find_elements(By.CLASS_NAME, "HeroImage.HeroImage--s")
    time.sleep(5)
    try:
        for mainImg in mainImgList:
            mainImg.click()
            time.sleep(5)

            # 메인 이미지 url
            mainImgUrl = mainImg.get_attribute("src")
            mainImgId = mainImg.get_attribute("data-element-index")

            img_url_info['mainImgUrl'] = mainImgUrl
            img_url_info['mainImgId'] = int(mainImgId) + 1

            # 메인 이미지 url DB 저장
            save_main_data(img_url_info)

            # 상세 이미지 url 가져오는 함수
            get_detail_img_url(driver)

        time.sleep(10)

    except Exception as e:
        print("e: ", e)
    pass


# 상세 이미지 url 가져오는 함수
def get_detail_img_url(driver):
    # 상세 페이지 탭
    tabList = driver.find_elements(By.CLASS_NAME,
                                   "Buttonstyled__ButtonStyled-sc-5gjk6l-0.izeZQM")

    # 객실 수 저장
    roomLen = int(re.sub(r'[^0-9]', '', tabList[2].text))

    # 객실 클릭
    tabList[2].click()
    time.sleep(2)

    # 상세(객실) 이미지 - 원본 이미지
    elements = driver.find_elements(By.CLASS_NAME,
                                    "Box-sc-kv6pi1-0 > img")
    count = 4
    while True:
        detailImgUrl = elements[count].get_attribute("src")
        img_url_info['detailImgUrl'] = detailImgUrl

        # 상세 이미지 개수 5개 가져오기 or 상세 이미지 개수가 5개보다 적은 경우 종료
        if (count == 9 or count > roomLen):
            # 상세 이미지 창 닫기
            driver.find_element(By.CLASS_NAME, "Box-sc-kv6pi1-0.dmiRkO").click()
            break
        save_detail_data(img_url_info)
        count += 1


# 스크롤 끝까지 내리기
SCROLL_PAUSE_TIME = 10

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # 끝까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(SCROLL_PAUSE_TIME)
    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")

    get_img_url(driver)

    # 마지막 스크롤일 때
    if new_height == last_height:
        try:
            # 다음 페이지로 이동
            next_button = driver.find_element(By.CSS_SELECTOR, "#paginationNext")
            if next_button.is_displayed():
                next_button.click()
                time.sleep(SCROLL_PAUSE_TIME)
            else:
                break  # 마지막 페이지인 경우 while loop 종료
        except:
            break  # 다음 페이지 버튼이 없는 경우 while loop 종료

    last_height = new_height

#
# def main():
#     get_img_url(driver)
#
#
# if __name__ == "__main__":
#     main()
