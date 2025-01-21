import urllib.request as request
import json
import re
import csv
import bs4
# ===============================Task 1===============================
spot_url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
mrt_url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

# 讀取網址
with request.urlopen(spot_url) as response:
    data=json.load(response)
spot_list = data["data"]["results"]
with request.urlopen(mrt_url) as response:
    data=json.load(response)
mrt_list = data["data"]

mrt_id_list=[]
spot_id_list=[]
image_list=[]
district_list=[]
station_list=[]
attraction_list={}


# 擷取第一章圖片
for spot in spot_list:
    regex = r"https:\/\/.*?\.jpg"
    images = spot["filelist"]
    first_img = re.findall(regex, images, re.IGNORECASE)[0]
    image_list.append(first_img)
    spot_id_list.append(spot["SERIAL_NO"])

# 用id對照district
for mrt in mrt_list:
    mrt_id_list.append(mrt["SERIAL_NO"])
    station_list.append(mrt["MRT"])
for i in range(len(spot_id_list)):
    for index, id in enumerate(mrt_id_list):
        if id in spot_id_list[i]:
            district_list.append(mrt_list[index]["address"][5:8])
            break

# 用id對照attraction
for i in range(len(spot_id_list)):
    for index, id in enumerate(mrt_id_list):
        if id in spot_id_list[i]:
            station = station_list[index]
            # 首次遇到該站名，先添加station為key
            if station not in attraction_list:
                attraction_list[station]=""
            if attraction_list[station]:  
                attraction_list[station] += ","
            attraction_list[station] += spot_list[i]["stitle"]
            break

# 寫入檔案
# f-string相當於JS的`${變數}`
with open("spot.csv","w",encoding="utf-8")as file:
    for i in range(len(spot_list)):
        file.write(f"{spot_list[i]["stitle"]},{district_list[i]},{spot_list[i]["longitude"]},{spot_list[i]["latitude"]},{image_list[i]}\n") 
with open("mrt.csv","w",encoding="utf-8")as file:
    for key,value in attraction_list.items():
        file.write(f"{key},{value}\n")


# ===============================Task 2===============================
ptt_url="https://www.ptt.cc/bbs/Lottery/index.html"
articles=[]
results=[]

# 讀取網址
def read_data(url):
    # 請求頭
    headers = {
                "Cookie": "over18=1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }
    req = request.Request(url, headers=headers)
    with request.urlopen(req) as response:
        return response.read().decode("utf-8")

# 抓取標題
def get_title(data):
    root = bs4.BeautifulSoup(data,"html.parser")
    titles=root.find_all("div", class_="title")
    for title in titles:
        if title.a !=None:
            articles.append({"title":title.a.string,"url":title.a["href"]})
    # 抓取上一頁連結
    prev_link=root.find("a",string="‹ 上頁")
    return prev_link["href"]

# 抓取推/噓數、時間
def get_detail(article):
    data = read_data("https://www.ptt.cc"+article["url"])
    root = bs4.BeautifulSoup(data,"html.parser")

    times=root.find_all("span", class_="article-meta-value")
    if times:
        publish_time = times[-1].string
    else:
        publish_time = ""

    count=0
    likes=root.find_all("span", class_="hl push-tag")
    for like in likes:
        if like.string == "推 ":
            count += 1

    dislikes=root.find_all("span", class_="f1 hl push-tag")
    for dislike in dislikes:
        if dislike.string == "噓 ":
            count -= 1
    return results.append({"title":article["title"],"like":count,"time":publish_time})

# 抓取前三頁
# 迭代變數不重要可設為_
for _ in range(3):  
    data = read_data(ptt_url)
    if not data:
        break

    # 清空前一頁內容
    articles.clear()
    new_url = get_title(data)

    for article in articles:
        details = get_detail(article)

    # 更新網址
    ptt_url = "https://www.ptt.cc" + new_url
        

# 寫入檔案
with open("article.csv","w",encoding="utf-8")as file:
    for result in results:
        file.write(f"{result["title"]},{result["like"]},{result["time"]}\n") 