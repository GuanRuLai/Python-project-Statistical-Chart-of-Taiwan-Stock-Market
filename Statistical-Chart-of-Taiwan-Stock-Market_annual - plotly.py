import requests
import csv
import os
import pandas as pd
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import plotly.graph_objects as go

# 自訂全年股票資料回傳方式(format in url:date=2021xx01)
def twoDigit(n):
    if n < 10:
        return_str = "0" + str(n)
    else:
        return_str = str(n)
    return return_str

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
url_head = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=2021"
url_tail = "01&stockNo=2317&response=html"
store_file = "stockYear_2021.csv"

dataFrame = pd.DataFrame() # 新增空的 DataFrame
if not os.path.isfile(store_file):
    for i in range(1, 13):
        url_combine = url_head + twoDigit(i) + url_tail
        print(url_combine)
        df_monthly = pd.read_html(url_combine, header = 1)[0] # 第一列為表頭
        # 結合各月股票資料
        dataFrame = pd.concat([dataFrame, df_monthly], ignore_index = True) # 忽略索引
        # 每次讀取資料延遲2秒，以免被認定為爬蟲
        time.sleep(2)
    dataFrame.to_csv(store_file, encoding = "utf-8")
    
# 讀取 csv 檔案並繪製統計圖
stock = pd.read_csv(store_file, encoding = "utf-8")
for i in range(len(stock["日期"])):
    stock["日期"][i] = convertDate(stock["日期"][i])
# 轉換日期字串為日期格式
stock["日期"] = pd.to_datetime(stock["日期"])
f = go.Figure()
f.add_trace(go.Scatter(x = stock["日期"], y = stock["收盤價"], name = "收盤價"))
f.add_trace(go.Scatter(x = stock["日期"], y = stock["最低價"], name = "最低價"))
f.add_trace(go.Scatter(x = stock["日期"], y = stock["最高價"], name = "最高價"))
f.update_layout(title = "2021年個股統計圖", showlegend = True)
f.show()
