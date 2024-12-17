import tkinter as tk
import tkinter.font as tkFont
import os
import sqlite3
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import csv
from pull import pull_file_from_device
import matplotlib.dates as mdates

conn = sqlite3.connect("zap_database")
cursor = conn.cursor()


class Page1(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.fontStyle = tkFont.Font(family="Helvetica", size=11, weight="normal", slant="roman")
        self.strVar1 = tk.StringVar()

        button1 = tk.Button(self, 
                            text="Download ZAP Database",
                            font=("Arial", 16),
                            command=self.get_zap_database,)
        button1.grid(column=0, row=0, padx=5, pady=10)


        button2 = tk.Button(self, 
                            text="Convert data to CSV",
                            font=("Arial", 16),
                            command=self.click_button1_2,
                            
                            )
        button2.grid(column=1, row=0, padx=5, pady=10)

        button3 = tk.Button(self, 
                            text="Plot Line Chart",
                            font=("Arial", 16),
                            command=lambda: self.click_plot_button("5T", 1)
                            )
        button3.grid(column=2, row=0, padx=5, pady=10)
        button4 = tk.Button(
            self,
            text="Step 4",
            font=("Arial", 16),
            command=lambda: print("Page 1 按鈕 4 被點擊"),
)
        button4.grid(column=0, row=1, padx=5, pady=10)
# button1_4.pack(side="left", pady=5, padx=10)

        button5 = tk.Button(
            self,
            text="Step 5",
            font=("Arial", 16),
            command=lambda: print("Page 1 按鈕 5 被點擊"),
        )
        button5.grid(column=1, row=1, padx=5, pady=10)



        button6 = tk.Button(
            self,
            text="15 minutes",
            font=("Arial", 16),
            command=lambda: self.click_plot_button("15T", 15),

        )
        button6.grid(column=0, row=10, padx=10, pady=60)

        button7 = tk.Button(
            self,
            text="30 minutes",
            font=("Arial", 16),
            command=lambda: self.click_plot_button("30T", 30),
            # command=lambda: print("間隔時間30分鐘"),
        )
        button7.grid(column=1, row=10, padx=10, pady=60)

        button8 = tk.Button(
            self,
            text="60 minutes",
            font=("Arial", 16),
            command=lambda: self.click_plot_button("60T", 60),
            # command=lambda: print("間隔時間60分鐘"),
        )
        button8.grid(column=2, row=10, padx=10, pady=60)

        self.label1 = tk.Label(
            master=self,
            bg="light grey",
            width=60,
            height=2,
            textvariable=self.strVar1,
            font=self.fontStyle,
        )
        self.label1.grid(row=30, column=1, padx=10, pady=40)

    def query_info(self):
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

    def get_zap_database(self):    
        user_downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        today_date = datetime.today().strftime("%Y_%m_%d")
        device_file = "/data/data/com.avalue.factory_test2/databases"  # 平板檔案路徑
        local_file = os.path.join(user_downloads_folder, f"zap_database_{today_date}")
        pull_file_from_device(
            device_file,
            local_file,),
        msg = "下載資料庫成功，檔名為zap_dabase_[下載日期]，存放Downloads資料夾"
        self.strVar1.set(msg)
        print("使用者下載資料庫成功，檔名為zap_dabase_[下載日期]，存放Downloads資料夾")
        
    
    def click_button1_2(self):
        self.query_info()
        msg = "SQL轉換為CSV檔案成功，檔名為mj.csv，存放於目前資料夾"
        self.strVar1.set(msg)
        print("使用者SQL轉換為CSV檔案成功，檔名為mj.csv，存放於目前資料夾")


    def click_plot_button(self,interval, time):
        db_data = pd.read_csv("mj.csv")

        df = pd.DataFrame(db_data)
        # 將df 轉出成csv檔案
        df["create_at"] = pd.to_datetime(df["create_at"], unit="ms")
        df.to_csv("mj_date.csv", index=False)

        # df = df.head(1000)
    
        plt.figure(figsize=(10, 5))
        plt.plot(df['create_at'], df['temperature'], marker='o', linestyle='-', label='Temperature Value')
        plt.plot(df['create_at'], df['humidity'], 'ro')

        plt.title("Temperature/Humidity over time")
        plt.xlabel("Time")
        plt.ylabel("Temperature/Humidity")
        plt.legend(['temperature','humidity'])

        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=time))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

        plt.xticks(rotation=90)  # 旋轉 X 軸標籤

        # 儲存為 JPG 圖檔
        plt.tight_layout()
        plt.savefig("line_chart.jpg", format="jpg", dpi=300)
        plt.show()
        # print("圖表已經成功儲存！")
        msg = "折線圖成功繪製，檔名為pm25_line_chart.jpg，存放於目前資料夾"
        self.strVar1.set(msg)
        print("目前折線圖成功繪製，檔名為pm25_line_chart.jpg，存放於目前資料夾")
