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
driver.get("https://www.naver.com")
# 로딩이 끝날 때까지 10초 기다리기
driver.implicitly_wait(10)

# 쇼핑 메뉴 클릭
driver.find_element(By.CSS_SELECTOR, 'a.nav.shop').click()
time.sleep(2)

# 검색창 클릭
search = driver.find_element(By.CSS_SELECTOR, 'input._searchInput_search_text_fSuJ6')
search.click()

# 검색어 입력
search.send_keys("녹두팩")
search.send_keys(Keys.ENTER)
