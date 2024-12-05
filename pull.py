import subprocess
import os
from datetime import datetime
import time

def pull_file_from_device(device_file_path, local_file_path):
    try:        
       
        # adb_path = input("請輸入adb.exe所在的完整路徑: ")

        # adb_path = r"C:\Users\wei\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

        # result = subprocess.run(
        #     [adb_path, "pull", device_file_path, local_file_path],
        #     capture_output=True,
        #     text=True,
        #     check=True,
        # )
        subprocess.run( ["adb", "root"],
           text=True,
            check=True,)
        
        time.sleep(2)
        

        result = subprocess.run(
            ["adb", "pull", device_file_path, local_file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        print("提取成功:", result.stdout)

    except subprocess.CalledProcessError as e:
        # 如果有錯誤發生，顯示錯誤訊息
        print("提取失敗:", e.stderr)



