import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

# 크롤링할 사이트 주소 = 카카오맵
url = "https://map.kakao.com/"

driver = webdriver.Chrome()
driver.get(url)

# 검색어를 입력
searchbox = driver.find_element(By.XPATH, "//input[@id='search.keyword.query']")
searchbox.send_keys("충북대 맛집")

# 검색
searchbutton = driver.find_element(By.XPATH, "//button[@id='search.keyword.submit']")
driver.execute_script("arguments[0].click();", searchbutton)
time.sleep(2)

# 페이지 URL 수집
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
moreviews = soup.find_all(name="a", attrs={"class":"moreview"})
page_urls = [moreview.get("href") for moreview in moreviews]

# 2페이지부터 5페이지까지 검색
    # 페이지 번호를 클릭
time.sleep(3)
a = driver.find_element(By.XPATH, '//a[@id="info.search.place.more"]')
a.click()

time.sleep(3)
for page_num in range(1,5):
    b = driver.find_element(By.XPATH, "//a[@id='info.search.page.no"+ str(page_num)+"']")
    b.click()

    time.sleep(1)
    print(page_num)