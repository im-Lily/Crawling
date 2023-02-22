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
checkIn = "2023-03-01"
checkOut = "2023-03-08"

# 웹페이지 해당 주소 이동
driver.get(
    f"https://www.agoda.com/ko-kr/search?city={city}&checkIn={checkIn}&los=7&rooms=1&adults=2&children=0&cid=1891463&locale=ko-kr&ckuid=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&prid=0&gclid=Cj0KCQiArsefBhCbARIsAP98hXRDutveTPNpWIfQLXDpoMElaN4JKjVtcEroqVIe_mgLos7C4swF9hAaAv3HEALw_wcB&currency=KRW&correlationId=60839d4e-ec58-4c59-937b-3f3710949d9c&analyticsSessionId=-7982247166164195812&pageTypeId=1&realLanguageId=9&languageId=9&origin=KR&tag=45b17d1d-e0b0-fe2a-ce90-5513829d856b&userId=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=hk-pc-2g-acm-web-user-cfc54bf5c-pw9vs&trafficGroupId=5&sessionId=15r2ueyomnlsg0dnubz31jmi&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&checkOut={checkOut}&priceCur=KRW&textToSearch=%EC%84%9C%EC%9A%B8&productType=-1&travellerType=1&familyMode=off")

# 로딩이 끝날 때까지 5초 기다리기
driver.implicitly_wait(5)

# 스크롤 끝까지 내리기
# SCROLL_PAUSE_TIME = 3
#
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(SCROLL_PAUSE_TIME)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#
#     if new_height == last_height:
#         try:
#             driver.find_element(By.CSS_SELECTOR, "#paginationNext").click()
#             time.sleep(SCROLL_PAUSE_TIME)
#         except:
#             break
#     last_height = new_height

# 메인, 상세(객실) 이미지 url 가져오기
imgUrlDict = {}
mainImages = driver.find_elements(By.CSS_SELECTOR, ".HeroImage")
try:
    for mainImage in mainImages:
        mainImage.click()
        time.sleep(2)
        # 메인 이미지 url
        mainImageUrl = mainImage.get_attribute("src")
        mainImageId = mainImage.get_attribute("data-element-index")
        print("mainImageUrl: ", mainImageUrl)
        print("mainImageId: ", mainImageId)
        imgUrlDict['mainImageUrl'] = mainImageUrl
        imgUrlDict['mainImageId'] = int(mainImageId) + 1

        print(
            "================================================================================================================")

        save_main_data(imgUrlDict)

        # 객실 클릭 TODO
        # 객실 사진수 가져오기
        elements = driver.find_elements(By.CLASS_NAME,
                                        "Buttonstyled__ButtonStyled-sc-5gjk6l-0.izeZQM")
        elements[2]. click()

        driver.find_element(By.XPATH,
                            "/html/body/div[17]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/button[2]/div/div/div/div/p").click()
        # 객실 이미지
        detailImages = driver.find_elements(By.XPATH,
                                            "/html/body/div[17]/div/div[2]/div/div/div[2]/div[2]/div[2]/div")

        # 객실 사진수 가져오기
        # elements = driver.find_elements(By.CLASS_NAME,
        #                                 "Buttonstyled__ButtonStyled-sc-5gjk6l-0.izeZQM")
        roomText = elements[2].text

        # 총 객실 사진수
        roomLen = int(re.sub(r'[^0-9]', '', roomText))

        # 객실 이미지 url 5개 가져오기
        for i in range(1, 6):
            driver.find_elements(By.CSS_SELECTOR,
                                 f".GalleryRefresh__ThumbnailScroller > div > div:nth-child({i})")  # 이게 뭐지
            detailImageUrl = driver.find_element(By.XPATH,
                                                 f"/html/body/div[17]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[{i}]/img").get_attribute(
                "src")
            # 객실 이미지 개수가 5개보다 작은 경우
            if (roomLen < i):
                detailImageUrl = driver.find_element(By.XPATH,
                                                     f"/html/body/div[17]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div[{roomLen}]/img").get_attribute(
                    "src")

            print("detailImageUrl: ", detailImageUrl)
            imgUrlDict['detailImageUrl'] = detailImageUrl

            save_detail_data(imgUrlDict)

        # 상세 이미지 창 닫기
        driver.find_element(By.XPATH, "/html/body/div[17]/div/div[2]/div/div/div[1]/button/div/div/div").click()

        # print("찾은 메인 이미지 개수 : ", len(imgUrlDict['mainImageUrl']))
        # print("찾은 상세 이미지 개수 : ", len(imgUrlDict['detailImageUrl']))

except Exception as e2:
    print("e2: ", e2)
    pass
