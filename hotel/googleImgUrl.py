import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
# 로딩이 끝날 때까지 10초 기다리기
driver.implicitly_wait(10)

# 검색창 클릭
search = driver.find_element(By.CSS_SELECTOR, 'input.gLFyf')
search.click()

# 검색어 입력
search.send_keys("호텔")
search.send_keys(Keys.ENTER)

# 스크롤 끝까지 내리기
SCROLL_PAUSE_TIME = 2

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            break
    last_height = new_height


# 이미지 url 가져오기
def img_url():
    links = []
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    try:
        for image in images:
            driver.execute_script("arguments[0].click();", image)
            time.sleep(2)
            imgUrl = driver.find_element(By.XPATH,
                                         '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[1]/div[2]/div[2]/div/a/img').get_attribute(
                "src")
            if (imgUrl != None):
                links.append(imgUrl)
    except Exception as e:
        print(e)
        pass

    print("찾은 이미지 개수 : ", len(links))

    driver.close()

    return links
