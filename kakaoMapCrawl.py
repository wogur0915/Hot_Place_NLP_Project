import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

excutable_path = 'chromedriver2.exe'

# 크롤링할 사이트 주소 = 카카오맵
url = "https://map.kakao.com/"

driver = webdriver.Chrome(executable_path=excutable_path)
driver.get(url)