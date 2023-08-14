import requests
import csv
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

# 自訂日期轉換格式：民國 to 西元
def convertDate(date):
    str1 = str(date)
    real_year = str1[0:3]
    convert_real_year = str(int(real_year) + 1911)
    real_date = convert_real_year + str1[4:6] + str1[7:9]
    return real_date

# 設定中文字型
fontManager.addfont("TaipeiSansTCBeta-Regular.ttf")
matplotlib.rc("font",family="Taipei Sans TC Beta")

# 建立 csv 檔案
store_file = "stockMonth_01.csv"
if not os.path.isfile(store_file):
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20210101&stockNo=2317&response=html"
    df = pd.read_html(url, header = 1)[0] # 第一列為表頭
    df.to_csv(store_file, encoding = "utf-8")
    
# 讀取 csv 檔案並繪製統計圖
stock = pd.read_csv(store_file, encoding = "utf-8")
for i in range(len(stock["日期"])):
    stock["日期"][i] = convertDate(stock["日期"][i])
# 轉換日期字串為日期格式
stock["日期"] = pd.to_datetime(stock["日期"])
stock.plot(kind = "line", figsize = (12, 6), x = "日期",
           y = ["收盤價", "最低價", "最高價"])
