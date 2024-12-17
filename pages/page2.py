import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
import pandas as pd
import tkinter.font as tkFont
from configparser import ConfigParser


# Config Parse
config = ConfigParser()
config.read("config.ini")
from configparser import ConfigParser

key = config["Environment"]["KEY"]
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


class Page2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # label = tk.Label(self, text="This is Page 2")
        # label.pack(pady=10)
        self.fontStyle = tkFont.Font(family="Helvetica", size=11, weight="normal", slant="roman")
        self.strVar1 = tk.StringVar()

        
        self.cal_start_label = tk.Label(self, text="Select Start Date")
        self.cal_start_label.grid(row=0, column=0, padx=0, pady=0)
        self.cal_start = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_start.grid(row=0, column=1, padx=0, pady=10)

        self.cal_end_label = tk.Label(self, text="Select End Date")
        self.cal_end_label.grid(row=1, column=0, padx=0, pady=0)
        self.cal_end = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal_end.grid(row=1, column=1, padx=0, pady=10)


        # 地區選單
        self.region_var = tk.StringVar()  # 地區變數
        self.region_menu = ttk.Combobox(self, textvariable=self.region_var, state="readonly")
        self.region_menu['values'] = list(location_data.keys())  # 設定地區選單選項
        self.region_menu.grid(row=2, column=0, padx=10, pady=30)
        self.region_menu.bind("<<ComboboxSelected>>", self.update_places)  # 綁定選擇事件

        # 地點選單
        self.place_var = tk.StringVar()  # 地點變數
        self.place_menu = ttk.Combobox(self, textvariable=self.place_var, state="readonly",width=15,height=15)
        self.place_menu.grid(row=2, column=1, padx=10, pady=30)
        self.place_menu.bind("<<ComboboxSelected>>", self.select_sitename)  # 綁定選擇事件

        # 預設值
        self.region_menu.set("Select Site Area")
        self.place_menu.set("Select Site Name ")

        
        button2_1 = tk.Button(
            self,
            text="Download PM2.5/10",
            font=("Arial", 16),
            command=lambda: self.download_pm25(),
        )
        button2_1.grid(column=0, row=4, padx=10, pady=10)


        button2_2 = tk.Button(
            self,
            text="PM2.5/10 Line Chart",
            font=("Arial", 16),
            command=lambda: self.click_plot_pm25_button(),

        )
        # button2_2.pack(pady=20)
        button2_2.grid(column=1, row=4, padx=10, pady=10)



        self.label2 = tk.Label(
            master=self,
            bg="light grey",
            width=60,
            height=2,
            textvariable=self.strVar1,
            font=self.fontStyle,
        )
        self.label2.grid(row=30, column=1, padx=10, pady=40)

    def update_places(self,event):
    # """根據所選地區更新地點下拉選單"""
        selected_region = self.region_var.get()
        # 獲取對應地點列表
        places = location_data.get(selected_region, [])
        # 清空舊選項
        self.place_menu['values'] = places
        # 重設預設值
        if places:
            self.place_var.set(places[0])
        else:
            self.place_var.set("")
        # print("PALCE:",self.place_var.get())    
        return self.place_var.get()


    selected_site=""
    def select_sitename(self,event):
    # """當使用者選擇地點時，印出選擇的地點"""
        global selected_site
        selected_site = self.place_var.get()
        # print("select_site",selected_site)       
        # print(f"選擇的地點: {selected_site}")


    def download_pm25(self):
        start_date = self.cal_start.get_date()
        end_date = self.cal_end.get_date()
        print("start",start_date,"end",end_date)
        url = f"https://data.moenv.gov.tw/api/v2/aqx_p_488?format=json&limit=2000&api_key={key}&filters=SiteName,EQ,{selected_site}|datacreationdate,GR,{start_date} 00:00:00|datacreationdate,LE,{end_date} 23:00:00"
        print("URL",url)
        r = requests.get(url)
        data=[]

        for time in r.json()['records']:
            data.append(((time['datacreationdate'], time['pm2.5_avg'], time['pm10_avg'])))

        df_pm25=pd.DataFrame(data=data)
        df_pm25.to_csv("pm25.csv", index=False)
        msg2 = "下載PM2.5/10資料並存成CSV檔案，檔名為pm25.csv，存放於目前資料夾"
        self.strVar1.set(msg2)
        print("使用者下載PM2.5/10資料並存成CSV檔案，檔名為pm25.csv，存放於目前資料夾")

    def click_plot_pm25_button(self):

        df = pd.read_csv('pm25.csv', header=None,skiprows=1)
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
        self.strVar1.set(msg)
        # self.strVar1.set(msg)
        print("目前pm2.5/10 折線圖成功繪製，檔名為pm25_chart.jpg，存放於目前資料夾")


 
        