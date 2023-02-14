import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.google.com/search?q=%ED%98%B8%ED%85%94&rlz=1C5CHFA_enKR1007KR1007&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjro_Hj65L9AhX3rlYBHdizC0MQ_AUoAnoECAEQBA&biw=1440&bih=686&dpr=2")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
imgs = soup.select(".rg_i Q4LuWd")
print(imgs)
for img in imgs:
    imgUrl = img.attrs['src']
    print(imgUrl)


