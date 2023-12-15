import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

restaurant_name = input()

# 크롤링할 사이트 주소 = 카카오맵
url = "https://map.kakao.com/"

driver = webdriver.Chrome()
driver.get(url)

# 검색어를 입력
searchbox = driver.find_element(By.XPATH, "//input[@id='search.keyword.query']")
searchbox.send_keys(restaurant_name)

# 검색
searchbutton = driver.find_element(By.XPATH, "//button[@id='search.keyword.submit']")
driver.execute_script("arguments[0].click();", searchbutton)
time.sleep(1)

# 첫 페이지 상세보기 URL 수집
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
moreviews = soup.find_all(name="a", attrs={"class":"moreview"})
page_urls = [moreview.get("href") for moreview in moreviews]


print("총", len(page_urls), "개의 맛집 정보를 수집합니다.")
print(page_urls)

# 리뷰 데이터 수집
review_data = []
page_url = page_urls[0]
driver.get(page_url)
time.sleep(2)

# 에러 처리 추가
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
contents_div = soup.find(name="div", attrs={"class":"evaluation_review"})
if contents_div is None:
    print(f"리뷰가 없는 페이지: {page_url}")

# 무한 스크롤링하여 모든 후기 수집
while True:
    try:
        # '후기 더보기' 버튼 클릭
        another_reviews = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[7]/div[3]/a')
        if another_reviews.text == '후기 더보기':
            another_reviews.click()
            time.sleep(1)
        else:
            break
    except:
        break

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    contents_div = soup.find(name="div", attrs={"class":"evaluation_review"})

    star_rates = contents_div.find_all(name="span", attrs={"class":"ico_star inner_star"})
    rates = [int(element['style'].split(':')[1].strip('%;')) / 20 for element in star_rates]

    reviews = contents_div.find_all(name="p", attrs={"class":"txt_comment"})
    for rate, review in zip(rates, reviews):
        review_data.append([rate, review.find(name="span").text])

# DataFrame 생성
df = pd.DataFrame(review_data, columns=['score', 'review'])
df['y'] = df['score'].apply(lambda x: 1 if x > 3 else 0)
print(df.shape)    

# CSV 파일로 저장
filename = f"review_data_{restaurant_name}.csv"
df.to_csv(filename, index=False, encoding='utf-8-sig')

# 드라이버 종료
driver.quit()