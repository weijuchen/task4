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

geocoding=[('Kuala Lumpur', 3.1516964, 101.6942371),  ('Ipoh', 4.5986817, 101.0900236), ('Malacca', 2.1942647, 102.2486651),('Penang', 5.2834958,100.4810318)]
 
Malaysia_cities = [
    "Kuala Lumpur",
    "Ipoh",
    "Malacca",
    "Penang",
]

class Page3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fontStyle = tkFont.Font(family="Helvetica", size=11, weight="normal", slant="roman")
        self.strVar1 = tk.StringVar()


        self.cal_MY_start_label = tk.Label(self, text="Select Start Date")
        self.cal_MY_start_label.grid(row=0, column=0, padx=0, pady=0)
        self.cal_MY_start = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_MY_start.grid(row=0, column=1, padx=0, pady=10)


        self.cal_MY_end_label = tk.Label(self, text="Select End Date")
        self.cal_MY_end_label.grid(row=1, column=0, padx=0, pady=0)
        self.cal_MY_end = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_MY_end.grid(row=1, column=1, padx=0, pady=10)



        # 地點選單
        self.city_var = tk.StringVar()  # 地點變數
        self.city_menu = ttk.Combobox(self, textvariable=self.city_var, values=Malaysia_cities, state="readonly",width=20,height=15)
        self.city_menu.grid(row=2, column=1, padx=10, pady=30)
        self.city_menu.bind("<<ComboboxSelected>>", self.select_city)  # 綁定選擇事件


        # 地區
        self.city_menu.set("Select City ")


        button3_1 = tk.Button(
            self,
            text="Download PM2.5",
            font=("Arial", 16),
            command=lambda: self.download_Malaysia_pm25(),
     
        )
        button3_1.grid(column=0, row=4, padx=5, pady=10)
        button3_2 = tk.Button(
            self,
            text="PM2.5 Line Chart",
            font=("Arial", 16),
            command=lambda: self.click_plot_pm25_MY_button(),
    
        )

        button3_2.grid(column=1, row=4, padx=5, pady=10)


        button3_3 = tk.Button(
            self,
            text="Last 10 Hours PM2.5 Data",
            font=("Arial", 16),
            command=lambda: self.view_current_pm25_MY_button(),
        )
        button3_3.grid(column=2, row=4, padx=5, pady=10)

        label3 = tk.Label(
            master=self,
            bg="light grey",
            width=70,
            height=2,
            textvariable=self.strVar1,
            font=self.fontStyle,
        )
        label3.grid(row=30, column=1, padx=10, pady=40)

    selected_city=""
    def select_city(self,event):
        global selected_city
        selected_city=self.city_var.get()
    
    def download_Malaysia_pm25(self):
        start_date_MY = self.cal_MY_start.get_date()
        end_date_MY = self.cal_MY_end.get_date()
        start_date_MY_unix=startDateConvertUnix(start_date_MY)
        end_date_MY_unix=endDateConvertUnix(end_date_MY)
        # print(f"start date unix: {start_date_MY_unix}")
        # print(f"end date unix: {end_date_MY_unix}")
        # print(f"selected city: {self.selected_city}")

        lat_MY=0
        lon_MY=0
        for name, lat,lon in geocoding:
            if name==self.selected_city:
                lat_MY=lat
                lon_MY=lon

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
        self.strVar1.set(msg3)
        print("使用者下載Malaysia PM2.5資料並存成CSV檔案，檔名為pm25_MY.csv，存放於目前資料夾")
            
    def click_plot_pm25_MY_button(self):
    
        df_MY_data = pd.read_csv('pm25_MY.csv', header=None, names=['Time', 'pm25'])
        df = pd.DataFrame(df_MY_data)
        df['Time'] = pd.to_datetime(df['Time'],unit='s')

        df['Time'] = df['Time'].dt.tz_localize('UTC')

        df['Time']=df['Time'].dt.tz_convert('Asia/Singapore').dt.tz_localize(None)
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
        self.strVar1.set(msg)
        print("目前折線圖成功繪製，檔名為pm25_MY_chart.jpg，存放於目前資料夾")


    def view_current_pm25_MY_button(self):
        now = datetime.now()
        start_time=now-timedelta(hours=11)
        start_date_MY_unix=int(start_time.timestamp())
        print(start_date_MY_unix)
        end_date_MY_unix=int(now.timestamp())
        lat_MY=0
        lon_MY=0
        for name, lat,lon in geocoding:
            if name==self.selected_city:
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
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
        plt.xticks(rotation=90)  # 調整 X 軸標籤角度以便顯示時間
        plt.tight_layout()  # 自動調整佈局
        # 顯示圖表
        plt.show()
        # 儲存為 JPG 圖檔
        plt.tight_layout()
        plt.savefig("pm25_MY_last_10hours_chart.jpg", format="jpg", dpi=300)
        plt.show()
        # print("圖表已經成功儲存！")
        msg = "折線圖成功繪製，檔名為pm25_MY_last_10hours_chart.jpg，存放於目前資料夾"
        self.strVar1.set(msg)
        print("目前折線圖成功繪製，檔名為pm25_MY_last_10hours_chart.jpg，存放於目前資料夾")

