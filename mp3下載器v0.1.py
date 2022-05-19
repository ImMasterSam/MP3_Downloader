# 問題:
# 1."音檔"資料夾問題
# 2.重複下載問題
# 3.下載歌曲使用函式，否則程式碼量過大
# 4.下載歌單功能
# 5.單曲下載要確定後才能下載
# 6.盡量簡化程式碼

# 模組們
import os.path, os
import tkinter as tk
from pytube import YouTube, Playlist, Search
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time

# 輸出位置
os.mkdir(r"C:\Users\User\Desktop\音檔")
folder = r"C:\Users\User\Desktop\音檔"

# 孤兒變數
global num
num = 0

# 建立tkinter圖片
def creatimg(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize( (img.width // 2, img.height // 2))
    #print("yes")

    return ImageTk.PhotoImage(img)

# 將格式換成mp3格式
def turntomp3():
    for filename in os.listdir(folder):
        #print(filename)
        infilename = os.path.join(folder, filename)
        #print(infilename)
        if not os.path.isfile(infilename): continue
        oldname = os.path.splitext(filename)
        newname = infilename.replace(oldname[1], '.mp3')
        os.rename(infilename, newname)

# tkinter 格式物件
class MP3app(tk.Tk):

    # 初始化 & 格式設定
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry("500x700")
        self.title("MP3下載器")
        self.switch_page(Startpage)
    
    # 摧毀頁面，建立新頁面
    def switch_page(self, frame_class):
        new_page = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_page
        self._frame.pack()

# 首頁的物件
class Startpage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 標籤 & 按鈕
        tk.Label(self
                ,text = "MP3下載器"
                ,font = ("Microsoft JhengHei", 22, "bold", "underline")
                ,pady = 10
                ,padx = 10).pack(pady=10)

        tk.Button(self
                 ,text = "線上搜尋"
                 ,font = ("Microsoft JhengHei", 16, "bold")
                 ,pady = 5
                 ,padx = 20
                 ,command = lambda: master.switch_page(Searchpage)).pack(pady=10)

        tk.Button(self
                 ,text = "單曲下載"
                 ,font = ("Microsoft JhengHei", 16, "bold")
                 ,pady = 5
                 ,padx = 20
                 ,command = lambda: master.switch_page(Onesongpage)).pack(pady=10)
 
        tk.Button(self
                 ,text = "歌單下載"
                 ,font = ("Microsoft JhengHei", 16, "bold")
                 ,pady = 5
                 ,padx = 20
                 ,command = lambda: master.switch_page(Multisongpage)).pack(pady=10)

# 上網搜尋頁面的物件
class Searchpage(tk.Frame):

    # 初始化版面
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 標籤 & 輸入串
        tk.Label(self
                ,text = "搜尋關鍵字:"
                ,font = ("Microsoft JhengHei", 20, "bold", "underline")
                ,pady = 10
                ,padx = 10).pack(pady=10)
        
        key = tk.Entry(self
                      ,width=35
                      ,font = ("", 16))
        key.pack()
        
        tk.Button(self
                 ,text = "搜尋"
                 ,font = ("Microsoft JhengHei", 12)
                 ,command = lambda: self.search(master, key.get())).pack(pady = 2)

    # 搜尋
    def search(self, master, key):

        s = Search(key).results

        def next(pic, s, title):
            global num
            num += 1
            changeimg = creatimg(s[num].thumbnail_url)
            pic.configure(image=changeimg)
            pic.image = changeimg
            #print(num)
            title.set(s[num%len(s)].title)

        if len(s) != 0:
            title = tk.StringVar(self)
            num = 0
            #print(len(s))
            imgTk = creatimg(s[num%len(s)].thumbnail_url)
            pic = tk.Label(self, image = imgTk)
            pic.image = imgTk
            pic.pack()
            title.set(s[num%len(s)].title)
            tk.Label(self
                    ,textvariable= title
                    ,font = ("Microsoft JhengHei", 8)
                    ,pady = 10
                    ,padx = 10).pack(pady=2)
            tk.Button(self
                     ,text = "下一項"
                     ,font = ("Microsoft JhengHei", 12)
                     ,command = lambda : next(pic, s, title)).pack(pady = 2)
            tk.Button(self
                     ,text = "確定並下載"
                     ,font = ("Microsoft JhengHei", 12)
                     ,command = lambda : self.downloadone(master, s[num%len(s)])).pack(pady = 2)   

    # 下載
    def downloadone(self, master, yt):

        try:
            dltxt = tk.StringVar(self)
            tk.Label(self
                    ,textvariable= dltxt
                    ,font = ("Microsoft JhengHei", 12)
                    ,pady = 10
                    ,padx = 10).pack(pady=10)
            yt.streams.get_audio_only().download(output_path = folder)
            dltxt.set("下載完成!")
            turntomp3()
            tk.Button(self
                        ,text = "返回"
                        ,font = ("Microsoft JhengHei", 12)
                        ,command = lambda: master.switch_page(Startpage)).pack(pady = 2)

        except:
            tk.Label(self
                    ,text = "無法下載!!!"
                    ,font = ("Microsoft JhengHei", 12)
                    ,pady = 10
                    ,padx = 10).pack(pady=10)
            tk.Button(self
                     ,text = "返回"
                     ,font = ("Microsoft JhengHei", 12)
                     ,command = lambda: master.switch_page(Startpage)).pack(pady = 2)

# 單曲下載頁面的物件
class Onesongpage(tk.Frame):

    # 初始化版面
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 標籤 & 輸入串
        tk.Label(self
                ,text = "請輸入網址:"
                ,font = ("Microsoft JhengHei", 20, "bold", "underline")
                ,pady = 10
                ,padx = 10).pack(pady=10)
        
        url = tk.Entry(self
                      ,width=35
                      ,font = ("", 16))
        
        url.pack()
        
        tk.Button(self
                 ,text = "確定"
                 ,font = ("Microsoft JhengHei", 12)
                 ,command = lambda: self.downloadone(master, url.get())).pack(pady = 2)

    # 下載
    def downloadone(self, master, url):
        
        if url != "":
            try:
                yt = YouTube(url)
                dltxt = tk.StringVar(self)
                title = tk.StringVar(self)
                imgTk = creatimg(yt.thumbnail_url)
                pic = tk.Label(self, image = imgTk)
                pic.image = imgTk
                pic.pack()
                title.set(yt.title)
                tk.Label(self
                        ,textvariable= title
                        ,font = ("Microsoft JhengHei", 8)
                        ,pady = 10
                        ,padx = 10).pack(pady=2)
                tk.Label(self
                        ,textvariable= dltxt
                        ,font = ("Microsoft JhengHei", 12)
                        ,pady = 10
                        ,padx = 10).pack(pady=10)
                yt.streams.get_audio_only().download(output_path = folder)
                dltxt.set("下載完成!")
                turntomp3()
                tk.Button(self
                         ,text = "返回"
                         ,font = ("Microsoft JhengHei", 12)
                         ,command = lambda: master.switch_page(Startpage)).pack(pady = 2)

            except:
                tk.Label(self
                        ,text = "無法下載!!!"
                        ,font = ("Microsoft JhengHei", 12)
                        ,pady = 10
                        ,padx = 10
                        ,bg = "#EF6351").pack(pady=10)
                tk.Button(self
                         ,text = "返回"
                         ,font = ("Microsoft JhengHei", 12)
                         ,command = lambda: master.switch_page(Startpage)).pack(pady = 2)

# 歌單下載頁面的物件
class Multisongpage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # 標籤 & 輸入串
        tk.Label(self
                ,text = "我還沒做好 XD"
                ,font = ("Microsoft JhengHei", 20, "bold", "underline")
                ,pady = 10
                ,padx = 10).pack(pady=10)
        
#        url = tk.Entry(self
#                      ,width=35
#                      ,font = ("", 16)).pack()
        tk.Button(self
                 ,text = "返回"
                 ,font = ("Microsoft JhengHei", 12)
                 ,command = lambda: master.switch_page(Startpage)).pack(pady = 2)

# 主程式運行
app = MP3app()
app.mainloop()
