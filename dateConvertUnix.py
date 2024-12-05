from datetime import datetime

# 用戶提供的日期字符串
def startDateConvertUnix(date):
    # date_string = "2024-11-07"

    # 將日期字符串轉換為 datetime 對象，並添加時間部分

    # 這裡我們使用 strptime() 方法解析字符串

    dt_object = datetime.strptime(date, "%Y-%m-%d")

    # 將時間設置為午夜（00:00:00）

    dt_object = dt_object.replace(hour=0, minute=0, second=0)

    # 轉換為 Unix 時間戳

    unix_timestamp = int(dt_object.timestamp())

    # 輸出結果
    
    # print(f"Unix 時間戳: {unix_timestamp}")
    return unix_timestamp

def endDateConvertUnix(date):
    # date_string = "2024-11-07"

    # 將日期字符串轉換為 datetime 對象，並添加時間部分

    # 這裡我們使用 strptime() 方法解析字符串

    dt_object = datetime.strptime(date, "%Y-%m-%d")

    # 將時間設置為午夜（00:00:00）

    dt_object = dt_object.replace(hour=23, minute=0, second=0)

    # 轉換為 Unix 時間戳

    unix_timestamp = int(dt_object.timestamp())

    # 輸出結果
    
    # print(f"Unix 時間戳: {unix_timestamp}")
    return unix_timestamp


# date="2024-11-06"
# startDateConvertUnix(date) 

# endDateConvertUnix(date) 

# from datetime import datetime

# # 用戶提供的日期字符串

# date_string = "2024-11-07"

# # 將日期字符串轉換為 datetime 對象，並添加時間部分

# # 這裡我們使用 strptime() 方法解析字符串

# dt_object = datetime.strptime(date_string, "%Y-%m-%d")

# # 將時間設置為午夜（00:00:00）

# dt_object = dt_object.replace(hour=0, minute=0, second=0)

# # 轉換為 Unix 時間戳

# unix_timestamp = int(dt_object.timestamp())

# # 輸出結果

# print(f"Unix 時間戳: {unix_timestamp}")

# from datetime import datetime

# # 定義日期字符串
# date_string = "2024-11-07 00:00:00"

# # 解析字符串為 datetime 對象
# dt_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

# # 轉換為 Unix 時間戳
# unix_timestamp = int(dt_object.timestamp())

# print(unix_timestamp)


# import datetime

# def dateConvertUnix():

# # 創建一個 datetime 對象
#     dt = datetime.datetime(2020, 11, 30, 22)
# # unix_timestamp = 1606488670
# # 2020-11-27 22:51:10
# # 將 datetime 對象轉換為 Unix 時間戳記
#     unix_timestamp = dt.timestamp()

# # 輸出結果
#     print(unix_timestamp)

# dateConvertUnix()