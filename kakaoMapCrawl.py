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