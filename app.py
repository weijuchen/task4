import tkinter as tk
from tkinter import ttk

# import my file pull_v5.py
# from pull_v6 import pull_file_from_device
# from air_api import get_pm25
from pull import pull_file_from_device
# from MY_air_api import download_MY_pm25
from dateConvertUnix import startDateConvertUnix,endDateConvertUnix
# from geocoding import geocoding_result

from tkcalendar import Calendar
# import pymysql
import os
import sqlite3
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone, timedelta
import tkinter.font as tkFont
import matplotlib.dates as mdates

import requests
from configparser import ConfigParser
import csv
import numpy as np
# D:\D_Download\zap_database

location_data = {
    "北部空品區": [
        "大同", "桃園", "大園", "基隆", "平鎮", "龍潭", "觀音", "汐止", "萬里", "新店", "土城",
        "板橋", "新莊", "菜寮", "林口", "淡水", "士林", "中山", "萬華", "古亭", "松山", "陽明",
        "三重", "中壢", "永和", "富貴角"
    ],
    "竹苗空品區": ["新竹", "竹東", "苗栗", "湖口", "三義", "頭份"],
    "中部空品區": ["南投", "線西", "二林", "大城", "埔里", "竹山", "豐原", "沙鹿", "大里", "忠明", "西屯", "彰化"],
    "雲嘉南空品區": [
        "嘉義", "新營", "善化", "安南", "臺南", "麥寮", "斗六", "崙背", "新港", "朴子", "臺西"
    ],
    "高屏空品區": [
        "左營", "楠梓", "林園", "美濃", "大寮", "鳳山", "復興", "仁武", "橋頭", "屏東", "潮州",
        "恆春", "小港", "前鎮", "前金"
    ],

    "宜蘭空品區": ["宜蘭", "冬山"],

    "花東空品區": ["臺東", "花蓮", "關山"],

        "其他": ["馬公", "金門", "馬祖"],
}

# geocoding=[('Kuala Lumpur', 3.1516964, 101.6942371), ('Petaling Jaya', 3.0991752, 101.6450232), ('George Town', 5.4141619, 100.3287352), ('Ipoh', 4.5986817, 101.0900236), 
#  ('Johor Bahru', 1.503555, 103.7495586), ('Klang', 49.3198, 
# 6.3722), ('Malacca', 2.1942647, 102.2486651), ('Kota Bharu', 6.12584, 102.2399785), ('Miri', 4.392739, 113.9880255), ('Bintulu', 3.1874261, 113.0472803)]


geocoding=[('Kuala Lumpur', 3.1516964, 101.6942371),  ('Ipoh', 4.5986817, 101.0900236), ('Malacca', 2.1942647, 102.2486651),('Penang', 5.2834958,100.4810318)]


# geocoding=[('Kuala Lumpur', 3.1516964, 101.6942371),  ('Ipoh', 4.5986817, 101.0900236), ('Malacca', 2.1942647, 102.2486651)]
# geocoding_SG=[('Singapore',1.2899175, 103.8519072)]

# geocoding=[('Kuala Lumpur', 3.1516964, 101.6942371), ('Petaling Jaya', 3.0991752, 101.6450232), ('George Town', 5.4141619, 100.3287352), ('Ipoh', 4.5986817, 101.0900236), 
#  ('Johor Bahru', 1.503555, 103.7495586), ('Klang', 49.3198, 
# 6.3722), ('Malacca', 2.1942647, 102.2486651), ('Kota Bharu', 6.12584, 102.2399785), ('Miri', 4.392739, 113.9880255), ('Bintulu', 3.1874261, 113.0472803)]



# Config Parse

config = ConfigParser()
config.read("config.ini")
from configparser import ConfigParser

key = config["Environment"]["KEY"]
open_weather_key = config["OPEN_WEATHER"]["API_KEY"]


conn = sqlite3.connect("zap_database")
# conn = sqlite3.connect("D:\D_Download\zap_database")
cursor = conn.cursor()



def query_info():
    query = "SELECT pm25,temperature,humidity,create_at FROM airqualitydata"
    # query = "SELECT pm25,temperature,humidity,create_at FROM airqualitydata"
    cursor.execute(query)
    data = cursor.fetchall()
    # print(data)

    with open("mj.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([header[0] for header in cursor.description])
        writer.writerows(data)
    print("匯出成功！")


interval = "5T"
time = 1


device_file = "/data/data/com.avalue.factory_test2/databases"  # 平板檔案路徑

user_downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

today_date = datetime.today().strftime("%Y_%m_%d")


local_file = os.path.join(user_downloads_folder, f"zap_database_{today_date}")
# print("local file path",local_file)
def get_zap_database():
    pull_file_from_device(
        device_file,
        local_file,),
    msg = "下載資料庫成功，檔名為zap_dabase_[下載日期]，存放Downloads資料夾"
    strVar1.set(msg)
    print("使用者下載資料庫成功，檔名為zap_dabase_[下載日期]，存放Downloads資料夾")


def click_button1_2():
    query_info()
    msg = "SQL轉換為CSV檔案成功，檔名為mj.csv，存放於目前資料夾"
    strVar1.set(msg)
    print("使用者SQL轉換為CSV檔案成功，檔名為mj.csv，存放於目前資料夾")


def click_plot_button(interval, time):
    db_data = pd.read_csv("mj.csv")

    df = pd.DataFrame(db_data)
    # 將df 轉出成csv檔案
    df["create_at"] = pd.to_datetime(df["create_at"], unit="ms")
    df.to_csv("mj_date.csv", index=False)

    # df = df.head(1000)
 
    plt.figure(figsize=(10, 5))
    plt.plot(df['create_at'], df['temperature'], marker='o', linestyle='-', label='Temperature Value')
    plt.plot(df['create_at'], df['humidity'], 'ro')
# pm25,temperature,humidity


    # df.to_csv("mj_head.csv", index=False)
    # df.set_index("create_at", inplace=True)

    # df_resampled = df.resample(interval).mean().reset_index()

    # X = list(df["create_at"])
    # Y = list(df["temperature"])

    # X = list(df_resampled["create_at"])
    # Y = list(df_resampled["temperature"])
    # plt.plot(X, Y, "r")
    # plt.plot(X, Y, "b-o")
    # plt.plot(X, Y, "ro--", linewidth=2, markersize=6)

    # plt.bar(X, Y, color="g")
    plt.title("Temperature/Humidity over time")
    plt.xlabel("Time")
    plt.ylabel("Temperature/Humidity")
    plt.legend(['temperature','humidity'])
# fig.gca().xaxis.set_major_formatter(mdates.DateFormatter(‘%Y-%m-%d’)) #設定x軸主刻度顯示格式（日期）
# fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14)) #設定x軸主刻度間距

    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=time))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

    plt.xticks(rotation=90)  # 旋轉 X 軸標籤

    # 儲存為 JPG 圖檔
    plt.tight_layout()
    plt.savefig("line_chart.jpg", format="jpg", dpi=300)
    plt.show()
    # print("圖表已經成功儲存！")
    msg = "折線圖成功繪製，檔名為pm25_line_chart.jpg，存放於目前資料夾"
    strVar1.set(msg)
    print("目前折線圖成功繪製，檔名為pm25_line_chart.jpg，存放於目前資料夾")


def update_places(event):
    """根據所選地區更新地點下拉選單"""
    selected_region = region_var.get()
    # 獲取對應地點列表
    places = location_data.get(selected_region, [])
    # 清空舊選項
    place_menu['values'] = places
    # 重設預設值
    if places:
        place_var.set(places[0])
    else:
        place_var.set("")
    print("PALCE:",place_var.get())    
    return place_var.get()
    # print(places.get())    
    # return places.get()

selected_site=""
def select_sitename(event):
# """當使用者選擇地點時，印出選擇的地點"""
    global selected_site
    selected_site = place_var.get()
    print("select_site",selected_site)
    
    print(f"選擇的地點: {selected_site}")
    # selected_site=site
    # return selected_site

def download_pm25():
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()
    print("start",start_date,"end",end_date)

    # site=select_sitename()
    # print("download_pm25 site: ",selected_site)
    url = f"https://data.moenv.gov.tw/api/v2/aqx_p_488?format=json&limit=2000&api_key={key}&filters=SiteName,EQ,{selected_site}|datacreationdate,GR,{start_date} 00:00:00|datacreationdate,LE,{end_date} 23:00:00"
   # url = f"https://data.moenv.gov.tw/api/v2/aqx_p_488?format=json&limit=2000&api_key={key}&filters=SiteName,EQ,土城|datacreationdate,GR,2024-10-01 00:00:00|datacreationdate,LE,2024-10-15 23:00:00"

   
   
    print("URL",url)
    # get_pm25()
    r = requests.get(url)
    data=[]

    for time in r.json()['records']:
        data.append(((time['datacreationdate'], time['pm2.5_avg'], time['pm10_avg'])))
    # print("here is the data",data)
    # print(type(data))

    # array=np.array(data)
    # df_pm25=pd.DataFrame(array)
    # column=['date','pm2.5','pm10']
    df_pm25=pd.DataFrame(data=data)
    # df_pm25=pd.DataFrame(columns=column,data=data)

    # print(df_pm25.iloc[1:])
    df_pm25.to_csv("pm25.csv", index=False)

    # print(f"here is the pm25/10 :{df_pm25}")

                            


    # data = {}
    # for time in r.json()["records"]:
    #     data[time["datacreationdate"]] = time["pm2.5_avg"]
    #     print("here is the data",data)
    
    # air_data = data
    # with open("pm25.csv", "w") as f:
    #     writer = csv.writer(f)
    #     for time, pm25,pm10 in air_data.items():
    #         writer.writerow([time, pm25,pm10])


    msg2 = "下載PM2.5/10資料並存成CSV檔案，檔名為pm25.csv，存放於目前資料夾"
    strVar1.set(msg2)
    print("使用者下載PM2.5/10資料並存成CSV檔案，檔名為pm25.csv，存放於目前資料夾")




def click_plot_pm25_button():
 
    # df = pd.read_csv('pm25.csv', header=None, names=['Time', 'pm25'])
    df = pd.read_csv('pm25.csv', header=None,skiprows=1)

    # print(df)
    # df['date'] = pd.to_datetime(df['date'])

  
  
    df.columns = ['date', 'pm2.5', 'pm10']
    df_sorted=df.sort_values(by='date')
    # print(df_sorted)
    # print(df)
    # 繪製折線圖
    plt.figure(figsize=(10, 5))
    plt.plot(df_sorted['date'], df_sorted['pm2.5'], marker='o', linestyle='-', label='PM2.5 Value')
    plt.plot(df_sorted['date'], df_sorted['pm10'], 'ro', linestyle='-',)
    
    
    
    
    # 添加圖表細節
    plt.xlabel('Date')  # X 軸標籤
    plt.ylabel('PM2.5/10')  # Y 軸標籤
    plt.title('PM2.5/10 Data Over Time')  # 圖表標題
    plt.grid(True)  # 顯示網格
    plt.legend('PM2.5','PM10')  # 顯示圖例
    plt.xticks(rotation=90)  # 調整 X 軸標籤角度以便顯示時間
    plt.tight_layout()  # 自動調整佈局

    # 顯示圖表
    plt.show()


    # 儲存為 JPG 圖檔
    plt.tight_layout()
    plt.savefig("pm25_chart.jpg", format="jpg", dpi=300)
    plt.show()
    print("圖表已經成功儲存！")
    msg = "PM2.5/10 折線圖成功繪製，檔名為pm25_chart.jpg，存放於目前資料夾"
    strVar1.set(msg)
    print("目前pm2.5/10 折線圖成功繪製，檔名為pm25_chart.jpg，存放於目前資料夾")


selected_city=""
def select_city(event):
    global selected_city
    selected_city=city_var.get()
    # how to print selected_city with a description
    # print("here is a selected city :", selected_city)
    # print(f"selected city: {selected_city}")
    # return selected_city


def download_Malaysia_pm25():
    start_date_MY = cal_MY_start.get_date()
    end_date_MY = cal_MY_end.get_date()
    start_date_MY_unix=startDateConvertUnix(start_date_MY)
    end_date_MY_unix=endDateConvertUnix(end_date_MY)
    print(f"start date unix: {start_date_MY_unix}")
    print(f"end date unix: {end_date_MY_unix}")
    print(f"selected city: {selected_city}")
    # city_index=geocoding.index(selected_city)
    # print(city_index)
    for name, lat,lon in geocoding:
        if name==selected_city:
            lat_MY=lat
            lon_MY=lon
            # print(f"MY: {lat_MY} {lon_MY}")

    # print("date type",type(start_date_MY))
    
    
# url=f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat=3.1516964&lon=101.6942371&start=1606488670&end=1606747870&appid={key}"
    url=f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat_MY}&lon={lon_MY}&start={start_date_MY_unix}&end={end_date_MY_unix}&appid={open_weather_key}"
    print("URL",url)
    r = requests.get(url)
    data = {}
    for time in r.json()["list"]:
        data[time["dt"]] = time["components"]["pm2_5"]
        # print("here is the data",data)
    pm25 = data
    with open("pm25_MY.csv", "w") as f:
        writer = csv.writer(f)
        for time, value in pm25.items():
            writer.writerow([time, value])
    msg3 = "下載Malaysia PM2.5資料並存成CSV檔案，檔名為pm25_MY.csv，存放於目前資料夾"
    strVar1.set(msg3)
    print("使用者下載Malaysia PM2.5資料並存成CSV檔案，檔名為pm25_MY.csv，存放於目前資料夾")
        
def click_plot_pm25_MY_button():
 
    df_MY_data = pd.read_csv('pm25_MY.csv', header=None, names=['Time', 'pm25'])
    df = pd.DataFrame(df_MY_data)
    df['Time'] = pd.to_datetime(df['Time'],unit='s')

    df['Time'] = df['Time'].dt.tz_localize('UTC')

    df['Time']=df['Time'].dt.tz_convert('Asia/Singapore').dt.tz_localize(None)

    # df['Time'] = df['Time'].dt.tz_localize('Asia/Taipei')  

    df.to_csv("pm_25_MY_date.csv", index=False)
    print("testing df",df)

    # 繪製折線圖
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['pm25'], marker='o', linestyle='-', label='PM2.5 Value')

    # 添加圖表細節
    plt.xlabel('Time')  # X 軸標籤
    plt.ylabel('PM2.5')  # Y 軸標籤
    plt.title(f'PM2.5 Data in {selected_city} Over Time')  # 圖表標題
    plt.grid(True)  # 顯示網格
    plt.legend()  # 顯示圖例



    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    # plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

    plt.xticks(rotation=90)  # 調整 X 軸標籤角度以便顯示時間
    plt.tight_layout()  # 自動調整佈局

    # 顯示圖表
    plt.show()


    # 儲存為 JPG 圖檔
    plt.tight_layout()
    plt.savefig("pm25_MY_chart.jpg", format="jpg", dpi=300)
    plt.show()
    # print("圖表已經成功儲存！")
    msg = "折線圖成功繪製，檔名為pm25_MY_chart.jpg，存放於目前資料夾"
    strVar1.set(msg)
    print("目前折線圖成功繪製，檔名為pm25_MY_chart.jpg，存放於目前資料夾")


def view_current_pm25_MY_button():
    now = datetime.now()
    start_time=now-timedelta(hours=10)
    
   
    start_date_MY_unix=int(start_time.timestamp())
    print(start_date_MY_unix)
    end_date_MY_unix=int(now.timestamp())
    # start_date_MY_unix=startDateConvertUnix(formatted_date)
    # end_date_MY_unix=endDateConvertUnix(formatted_start_time)   
    # print(formatted_date)
    for name, lat,lon in geocoding:
        if name==selected_city:
            lat_MY=lat
            lon_MY=lon
    url=f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat_MY}&lon={lon_MY}&start={start_date_MY_unix}&end={end_date_MY_unix}&appid={open_weather_key}"        
    r = requests.get(url)
    print(r.json())
    data = {}
    for time in r.json()["list"]:
        data[time["dt"]] = time["components"]["pm2_5"]
        # print("here is the data",data)
    pm25 = data
    with open("pm25_MY_current.csv", "w") as f:
        writer = csv.writer(f)
        for time, value in pm25.items():
            writer.writerow([time, value]) 
    print("使用者下載目前Malaysia PM2.5資料並存成CSV檔案，檔名為pm25_MY_current.csv，存放於目前資料夾")          
    df_MY_data = pd.read_csv('pm25_MY_current.csv', header=None, names=['Time', 'pm25'])
    df = pd.DataFrame(df_MY_data)
    df['Time'] = pd.to_datetime(df['Time'],unit='s')

    df['Time'] = df['Time'].dt.tz_localize('UTC')

    df['Time']=df['Time'].dt.tz_convert('Asia/Singapore').dt.tz_localize(None)
    df.to_csv("pm_25_MY_current_date.csv", index=False)
    print("testing df",df)

    # 繪製折線圖
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['pm25'], marker='o', linestyle='-', label='PM2.5 Value')

    # 添加圖表細節
    plt.xlabel('Time')  # X 軸標籤
    plt.ylabel('PM2.5')  # Y 軸標籤
    plt.title(f'PM2.5 Data in {selected_city} Over Time')  # 圖表標題
    plt.grid(True)  # 顯示網格
    plt.legend()  # 顯示圖例



    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    # plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

    plt.xticks(rotation=90)  # 調整 X 軸標籤角度以便顯示時間
    plt.tight_layout()  # 自動調整佈局

    # 顯示圖表
    plt.show()


    # 儲存為 JPG 圖檔
    plt.tight_layout()
    plt.savefig("pm25_MY_chart.jpg", format="jpg", dpi=300)
    plt.show()
    # print("圖表已經成功儲存！")
    msg = "折線圖成功繪製，檔名為pm25_MY_current_chart.jpg，存放於目前資料夾"
    strVar1.set(msg)
    print("目前折線圖成功繪製，檔名為pm25_MY_current_chart.jpg，存放於目前資料夾")


def download_SG_pm25():
    start_date_SG = cal_SG_start.get_date()
    end_date_SG = cal_SG_end.get_date()
    start_date_SG_unix=startDateConvertUnix(start_date_SG)
    end_date_SG_unix=endDateConvertUnix(end_date_SG)
    print(f"start date unix: {start_date_SG_unix}")
    print(f"end date unix: {end_date_SG_unix}")
    # print(f"selected city: {selected_city}")
    # city_index=geocoding.index(selected_city)
    # print(city_index)
    lat_SG=1.2899175
    lon_SG=103.8519072

    
# url=f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat=3.1516964&lon=101.6942371&start=1606488670&end=1606747870&appid={key}"
    url=f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat_SG}&lon={lon_SG}&start={start_date_SG_unix}&end={end_date_SG_unix}&appid={open_weather_key}"
    print("URL",url)
    r = requests.get(url)
    data = {}
    for time in r.json()["list"]:
        data[time["dt"]] = time["components"]["pm2_5"]
        # print("here is the data",data)
    pm25 = data
    with open("pm25_SG.csv", "w") as f:
        writer = csv.writer(f)
        for time, value in pm25.items():
            writer.writerow([time, value])
    msg3 = "下載Singapore PM2.5資料，並存成CSV檔案，檔名為pm25_SG.csv，存放於目前資料夾"
    strVar1.set(msg3)
    print("使用者下載Singapore PM2.5資料並存成CSV檔案，檔名為pm25_SG.csv，存放於目前資料夾")
  
def click_plot_pm25_SG_button():
 
    df_SG_data = pd.read_csv('pm25_SG.csv', header=None, names=['Time', 'pm25'])
    df = pd.DataFrame(df_SG_data)
    df['Time'] = pd.to_datetime(df['Time'],unit='s')

    df['Time'] = df['Time'].dt.tz_localize('UTC')

    df['Time']=df['Time'].dt.tz_convert('Asia/Singapore').dt.tz_localize(None)


    # df['Time'] = df['Time'].dt.tz_localize('Asia/Taipei')  

    df.to_csv("pm_25_SG_date.csv", index=False)
    print("testing df",df)

    # 繪製折線圖
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['pm25'], marker='o', linestyle='-', label='PM2.5 Value')

    # 添加圖表細節
    plt.xlabel('Time')  # X 軸標籤
    plt.ylabel('PM2.5')  # Y 軸標籤
    plt.title('PM2.5 Data in Singapore Over Time')  # 圖表標題
    plt.grid(True)  # 顯示網格
    plt.legend()  # 顯示圖例

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    # plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

    plt.xticks(rotation=90)  # 調整 X 軸標籤角度以便顯示時間
    plt.tight_layout()  # 自動調整佈局

    # 顯示圖表
    plt.show()


    # 儲存為 JPG 圖檔
    plt.tight_layout()
    plt.savefig("pm25_SG_chart.jpg", format="jpg", dpi=300)
    plt.show()
    # print("圖表已經成功儲存！")
    msg = "折線圖成功繪製，檔名為pm25_SG_chart.jpg，存放於目前資料夾"
    strVar1.set(msg)
    print("目前折線圖成功繪製，檔名為pm25_SG_chart.jpg，存放於目前資料夾")



root = tk.Tk()
root.title("GUI Ver1 @v0.04 2024-11-27")
root.geometry("800x400")


notebook = ttk.Notebook(root)


tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="ZAP資料")

strVar1 = tk.StringVar()
# from MY_air_api import strVar2
# strVar2 = tk.StringVar()
fontStyle = tkFont.Font(family="Helvetica", size=11, weight="normal", slant="roman")

button1_1 = tk.Button(
    tab1,
    text="Download ZAP Database",
    font=("Arial", 16),
    # command=lambda: pull_file_from_device(
    #     "/data/data/com.avalue.factory_test2/databases",
    #     os.path.join(user_downloads_folder, f"newname_{today_date}"),
    # ),
    command=get_zap_database,
    # command=query_info,
    # command=lambda: print("Page 1 按鈕 1 被點擊"),
)
# button1_1.pack(side='left',pady=5,padx=10)
button1_1.grid(column=0, row=0, padx=5, pady=10)

button1_2 = tk.Button(
    tab1,
    text="Convert data to CSV",
    font=("Arial", 16),
    command=click_button1_2,
    # command=query_info,
    # command=lambda: plot_bar_chart("5T", 5),
    # command=lambda: print("Page 1 按鈕 2 被點擊"),
)
button1_2.grid(column=1, row=0, padx=5, pady=10)
# button1_2.pack(side="left", pady=5, padx=10)
button1_3 = tk.Button(
    tab1,
    text="Plot Line Chart",
    font=("Arial", 16),
    command=lambda: click_plot_button("5T", 1),
    # command=click_button1_3,
    # command=lambda: plot_bar_chart("5T", 5),
)
button1_3.grid(column=2, row=0, padx=5, pady=10)
# button1_3.pack(side="left", pady=5, padx=10)
button1_4 = tk.Button(
    tab1,
    text="Step 4",
    font=("Arial", 16),
    command=lambda: print("Page 1 按鈕 4 被點擊"),
)
button1_4.grid(column=0, row=1, padx=5, pady=10)
# button1_4.pack(side="left", pady=5, padx=10)

button1_5 = tk.Button(
    tab1,
    text="Step 5",
    font=("Arial", 16),
    command=lambda: print("Page 1 按鈕 5 被點擊"),
)
button1_5.grid(column=1, row=1, padx=5, pady=10)
# button1_5.pack(side="left", pady=5, padx=10)


button1_6 = tk.Button(
    tab1,
    text="15 minutes",
    font=("Arial", 16),
    command=lambda: click_plot_button("15T", 15),
    # command=plot_bar_chart(15),
    # command=lambda: print("間隔時間15分鐘"),
)
button1_6.grid(column=0, row=10, padx=10, pady=60)

button1_7 = tk.Button(
    tab1,
    text="30 minutes",
    font=("Arial", 16),
    command=lambda: click_plot_button("30T", 30),
    # command=lambda: print("間隔時間30分鐘"),
)
button1_7.grid(column=1, row=10, padx=10, pady=60)

button1_8 = tk.Button(
    tab1,
    text="60 minutes",
    font=("Arial", 16),
    command=lambda: click_plot_button("60T", 60),
    # command=lambda: print("間隔時間60分鐘"),
)
button1_8.grid(column=2, row=10, padx=10, pady=60)

# frame1 = tk.LabelFrame(root, text='Print messages', width=450, height=50)
label1 = tk.Label(
    master=tab1,
    bg="light grey",
    width=60,
    height=2,
    textvariable=strVar1,
    font=fontStyle,
)
label1.grid(row=30, column=1, padx=10, pady=40)


tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="臺灣PM2.5資料")



cal_start_label = tk.Label(tab2, text="Select Start Date")
cal_start_label.grid(row=0, column=0, padx=0, pady=0)
# cal_start_label.grid(row=0, column=0, padx=0, pady=0,sticky="w")
cal_start = Calendar(tab2, selectmode='day', date_pattern='yyyy-mm-dd')
cal_start.grid(row=0, column=1, padx=0, pady=10)
# cal_start.grid(row=0, column=1, padx=0, pady=0,sticky="w")

cal_end_label = tk.Label(tab2, text="Select End Date")
cal_end_label.grid(row=1, column=0, padx=0, pady=0)
# cal_end_label.grid(row=1, column=0, padx=0, pady=0,sticky="w")
cal_end = Calendar(tab2, selectmode='day', date_pattern='yyyy-mm-dd')
cal_end.grid(row=1, column=1, padx=0, pady=10)
# cal_end.grid(row=1, column=1, padx=0, pady=0,sticky="w")

# 地區選單
region_var = tk.StringVar()  # 地區變數
region_menu = ttk.Combobox(tab2, textvariable=region_var, state="readonly")
region_menu['values'] = list(location_data.keys())  # 設定地區選單選項
region_menu.grid(row=2, column=0, padx=10, pady=30)
region_menu.bind("<<ComboboxSelected>>", update_places)  # 綁定選擇事件

# 地點選單
place_var = tk.StringVar()  # 地點變數
place_menu = ttk.Combobox(tab2, textvariable=place_var, state="readonly",width=15,height=15)
place_menu.grid(row=2, column=1, padx=10, pady=30)
place_menu.bind("<<ComboboxSelected>>", select_sitename)  # 綁定選擇事件

# 預設值
region_menu.set("Select Site Area")
place_menu.set("Select Site Name ")


button2_1 = tk.Button(
    tab2,
    text="Download PM2.5/10",
    font=("Arial", 16),
    command=lambda: download_pm25(),
    # command=lambda: print("Page 2 按鈕 2 被點擊"),
)
button2_1.grid(column=0, row=4, padx=10, pady=10)


button2_2 = tk.Button(
    tab2,
    text="PM2.5/10 Line Chart",
    font=("Arial", 16),
    command=lambda: click_plot_pm25_button(),
    # command=lambda: print("Page 2 按鈕 2 被點擊"),
)
# button2_2.pack(pady=20)
button2_2.grid(column=1, row=4, padx=10, pady=10)



label2 = tk.Label(
    master=tab2,
    bg="light grey",
    width=60,
    height=2,
    textvariable=strVar1,
    font=fontStyle,
)
label2.grid(row=30, column=1, padx=10, pady=40)
# button2_1.grid(column=1, row=1, padx=10, pady=10)

# label2.pack(padx=10, pady=40)




tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="馬來西亞PM2.5資料")
Malaysia_cities = [
    "Kuala Lumpur",
    "Ipoh",
    "Malacca",
    "Penang",
]
# Malaysia_cities = [
#     "Kuala Lumpur",
#     "Petaling Jaya",
#     "George Town",
#     "Ipoh",
#     "Johor Bahru",
#     "Klang",
#     "Malacca",
#     "Kota Bharu",
#     "Miri",
#     "Bintulu"
# ]

cal_MY_start_label = tk.Label(tab3, text="Select Start Date")
cal_MY_start_label.grid(row=0, column=0, padx=0, pady=0)
# cal_start_label.grid(row=0, column=0, padx=0, pady=0,sticky="w")
cal_MY_start = Calendar(tab3, selectmode='day', date_pattern='yyyy-mm-dd')
cal_MY_start.grid(row=0, column=1, padx=0, pady=10)
# cal_start.grid(row=0, column=1, padx=0, pady=0,sticky="w")

cal_MY_end_label = tk.Label(tab3, text="Select End Date")
cal_MY_end_label.grid(row=1, column=0, padx=0, pady=0)
# cal_end_label.grid(row=1, column=0, padx=0, pady=0,sticky="w")
cal_MY_end = Calendar(tab3, selectmode='day', date_pattern='yyyy-mm-dd')
cal_MY_end.grid(row=1, column=1, padx=0, pady=10)
# cal_end.grid(row=1, column=1, padx=0, pady=0,sticky="w")


# 地點選單
city_var = tk.StringVar()  # 地點變數
city_menu = ttk.Combobox(tab3, textvariable=city_var, values=Malaysia_cities, state="readonly",width=20,height=15)
# city_menu = ttk.Combobox(tab3, values=Malaysia_locations,width=15,height=15)
# city_menu = ttk.Combobox(tab3, textvariable=city_var, state="readonly",width=15,height=15)
city_menu.grid(row=2, column=1, padx=10, pady=30)
city_menu.bind("<<ComboboxSelected>>", select_city)  # 綁定選擇事件


# 地區
city_menu.set("Select City ")


button3_1 = tk.Button(
    tab3,
    text="Download PM2.5",
    font=("Arial", 16),
    command=lambda: download_Malaysia_pm25(),
    # command=lambda: print("Page 3 按鈕 1 被點擊"),
)
button3_1.grid(column=0, row=4, padx=5, pady=10)


button3_2 = tk.Button(
    tab3,
    text="PM2.5 Line Chart",
    font=("Arial", 16),
    command=lambda: click_plot_pm25_MY_button(),
    # command=lambda: print("Page 3 按鈕 2 被點擊"),
)
# button2_2.pack(pady=20)
button3_2.grid(column=1, row=4, padx=5, pady=10)


button3_3 = tk.Button(
    tab3,
    text="View Current PM2.5 ",
    font=("Arial", 16),
    command=lambda: view_current_pm25_MY_button(),
    # command=lambda: print("Page 3 按鈕 3 被點擊"),
)
# button2_2.pack(pady=20)
button3_3.grid(column=2, row=4, padx=5, pady=10)

label3 = tk.Label(
    master=tab3,
    bg="light grey",
    width=70,
    height=2,
    textvariable=strVar1,
    font=fontStyle,
)
label3.grid(row=30, column=1, padx=10, pady=40)


# notebook.grid(row=0, column=0, padx=10, pady=10)
# notebook.pack(expand=True, fill="both")

tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="新加坡PM2.5資料")


cal_SG_start_label = tk.Label(tab4, text="Select Start Date")
cal_SG_start_label.grid(row=0, column=0, padx=0, pady=0)
# cal_start_label.grid(row=0, column=0, padx=0, pady=0,sticky="w")
cal_SG_start = Calendar(tab4, selectmode='day', date_pattern='yyyy-mm-dd')
cal_SG_start.grid(row=0, column=1, padx=0, pady=10)
# cal_start.grid(row=0, column=1, padx=0, pady=0,sticky="w")

cal_SG_end_label = tk.Label(tab4, text="Select End Date")
cal_SG_end_label.grid(row=1, column=0, padx=0, pady=0)
# cal_end_label.grid(row=1, column=0, padx=0, pady=0,sticky="w")
cal_SG_end = Calendar(tab4, selectmode='day', date_pattern='yyyy-mm-dd')
cal_SG_end.grid(row=1, column=1, padx=0, pady=10)
# cal_end.grid(row=1, column=1, padx=0, pady=0,sticky="w")


button4_1 = tk.Button(
    tab4,
    text="Download PM2.5",
    font=("Arial", 16),
    command=lambda: download_SG_pm25(),
    # command=lambda: print("Page 4 按鈕 1 被點擊"),
)
button4_1.grid(column=0, row=4, padx=10, pady=10)


button4_2 = tk.Button(
    tab4,
    text="PM2.5 Line Chart",
    font=("Arial", 16),
    command=lambda: click_plot_pm25_SG_button(),
    # command=lambda: print("Page 4 按鈕 2 被點擊"),
)
# button2_2.pack(pady=20)
button4_2.grid(column=1, row=4, padx=10, pady=10)



label4 = tk.Label(
    master=tab4,
    bg="light grey",
    width=70,
    height=2,
    textvariable=strVar1,
    font=fontStyle,
)
label4.grid(row=30, column=1, padx=10, pady=40)


notebook.grid(row=0, column=0, padx=10, pady=10)



tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="其他國家PM2.5資料")
root.mainloop()
