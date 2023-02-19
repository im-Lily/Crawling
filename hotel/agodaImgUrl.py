import time

from selenium import webdriver
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
checkIn = "2023-03-01"
checkOut = "2023-03-08"

# 웹페이지 해당 주소 이동
driver.get(
    f"https://www.agoda.com/ko-kr/search?city={city}&checkIn={checkIn}&los=7&rooms=1&adults=2&children=0&cid=1891463&locale=ko-kr&ckuid=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&prid=0&gclid=Cj0KCQiArsefBhCbARIsAP98hXRDutveTPNpWIfQLXDpoMElaN4JKjVtcEroqVIe_mgLos7C4swF9hAaAv3HEALw_wcB&currency=KRW&correlationId=60839d4e-ec58-4c59-937b-3f3710949d9c&analyticsSessionId=-7982247166164195812&pageTypeId=1&realLanguageId=9&languageId=9&origin=KR&tag=45b17d1d-e0b0-fe2a-ce90-5513829d856b&userId=8f4ef8c2-a7ba-446b-b2f5-3f299164454f&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=hk-pc-2g-acm-web-user-cfc54bf5c-pw9vs&trafficGroupId=5&sessionId=15r2ueyomnlsg0dnubz31jmi&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&checkOut={checkOut}&priceCur=KRW&textToSearch=%EC%84%9C%EC%9A%B8&productType=-1&travellerType=1&familyMode=off")

# 로딩이 끝날 때까지 5초 기다리기
driver.implicitly_wait(5)

# 스크롤 끝까지 내리기
# SCROLL_PAUSE_TIME = 1
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
#         except:
#             break
#     last_height = new_height

# 메인, 상세 이미지 url 가져오기
mainImgLinks = []
detailImageLinks = []
mainImages = driver.find_elements(By.CSS_SELECTOR, ".HeroImage")
try:
    for mainImage in mainImages:
        mainImage.click()
        time.sleep(2)
        mainImageUrl = mainImage.get_attribute("src")
        print(mainImageUrl)
        if (mainImageUrl != None):
            mainImgLinks.append(mainImageUrl)

        # 객실 클릭
        driver.find_element(By.XPATH,
                            "/html/body/div[17]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/button[2]/div/div/div/div/p").click()
        # TODO 객실 이미지 개수만큼 반복해서 객실 이미지 5개 가져오기
        detailImages = driver.find_elements(By.CSS_SELECTOR, ".GalleryRefresh__ThumbnailScroller")
        for detailImage in detailImages:
            driver.execute_script("arguments[0].click();", detailImage)
            detailImageUrl = driver.find_element(By.XPATH, "/html/body/div[17]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/img").get_attribute("src")
            print("> ", detailImageUrl)

    print("찾은 메인 이미지 개수 : ", len(mainImgLinks))

except Exception as e:
    print(e)
    pass
