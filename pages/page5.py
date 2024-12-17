import tkinter as tk

class Page5(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="This is Page 5")
        label.pack(pady=10)

        button1 = tk.Button(self, text="Function 5_1", command=self.function1)
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Function 5_2", command=self.function2)
        button2.pack(pady=5)

        button3 = tk.Button(self, text="Function 5_3", command=self.function3)
        button3.pack(pady=5)

    def function1(self):
        print("Function 5_1 executed")

    def function2(self):
        print("Function 5_2 executed")

    def function3(self):
        print("Function 5_3 executed")