import tkinter as tk
from tkinter import ttk
from pages.page1 import Page1
from pages.page2 import Page2
from pages.page3 import Page3
from pages.page4 import Page4
from pages.page5 import Page5

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("GUI Ver1 @v0.1.0 2024-12-18")
        self.master.geometry("400x300")    

    # 創建 Notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # 創建分頁
        self.create_pages()

    def create_pages(self):
        # 添加各個分頁到 Notebook
        page1 = Page1(self.notebook)
        page2 = Page2(self.notebook)
        page3 = Page3(self.notebook)
        page4 = Page4(self.notebook)
        page5 = Page5(self.notebook)

        self.notebook.add(page1, text="ZAP資料")
        self.notebook.add(page2, text="臺灣PM2.5資料")
        self.notebook.add(page3, text="馬來西亞PM2.5資料")
        self.notebook.add(page4, text="新加坡PM2.5資料")
        self.notebook.add(page5, text="其他國家PM2.5資料")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
