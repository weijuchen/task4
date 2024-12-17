import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from configparser import ConfigParser
import tkinter.font as tkFont
from dateConvertUnix import startDateConvertUnix,endDateConvertUnix
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Config Parse
config = ConfigParser()
config.read("config.ini")
from configparser import ConfigParser

open_weather_key = config["OPEN_WEATHER"]["API_KEY"]

class Page4(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fontStyle = tkFont.Font(family="Helvetica", size=11, weight="normal", slant="roman")
        self.strVar1 = tk.StringVar()
        self.cal_SG_start_label = tk.Label(self, text="Select Start Date")
        self.cal_SG_start_label.grid(row=0, column=0, padx=0, pady=0)
        self.cal_SG_start = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_SG_start.grid(row=0, column=1, padx=0, pady=10)

        self.cal_SG_end_label = tk.Label(self, text="Select End Date")
        self.cal_SG_end_label.grid(row=1, column=0, padx=0, pady=0)
        self.cal_SG_end = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_SG_end.grid(row=1, column=1, padx=0, pady=10)


        button4_1 = tk.Button(
            self,
            text="Download PM2.5",
            font=("Arial", 16),
            command=lambda: self.download_SG_pm25(),
            # command=lambda: print("Page 4 按鈕 1 被點擊"),
        )
        button4_1.grid(column=0, row=4, padx=10, pady=10)


        button4_2 = tk.Button(
            self,
            text="PM2.5 Line Chart",
            font=("Arial", 16),
            command=lambda: self.click_plot_pm25_SG_button(),
            # command=lambda: print("Page 4 按鈕 2 被點擊"),
        )
 
        button4_2.grid(column=1, row=4, padx=10, pady=10)



        label4 = tk.Label(
            master=self,
            bg="light grey",
            width=70,
            height=2,
            textvariable=self.strVar1,
            font=self.fontStyle,
        )
        label4.grid(row=30, column=1, padx=10, pady=40)


    
    def download_SG_pm25(self):
        start_date_SG = self.cal_SG_start.get_date()
        end_date_SG = self.cal_SG_end.get_date()
        start_date_SG_unix=startDateConvertUnix(start_date_SG)
        end_date_SG_unix=endDateConvertUnix(end_date_SG)
        print(f"start date unix: {start_date_SG_unix}")
        print(f"end date unix: {end_date_SG_unix}")
 
        lat_SG=1.2899175
        lon_SG=103.8519072

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
        self.strVar1.set(msg3)
        print("使用者下載Singapore PM2.5資料並存成CSV檔案，檔名為pm25_SG.csv，存放於目前資料夾")
    
    def click_plot_pm25_SG_button(self):
    
        df_SG_data = pd.read_csv('pm25_SG.csv', header=None, names=['Time', 'pm25'])
        df = pd.DataFrame(df_SG_data)
        df['Time'] = pd.to_datetime(df['Time'],unit='s')

        df['Time'] = df['Time'].dt.tz_localize('UTC')

        df['Time']=df['Time'].dt.tz_convert('Asia/Singapore').dt.tz_localize(None)

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
        self.strVar1.set(msg)
        print("目前折線圖成功繪製，檔名為pm25_SG_chart.jpg，存放於目前資料夾")
        
