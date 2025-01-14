import math
from functools import reduce
print("===Task 1===");
def find_and_print(messages, current_station):
    # 所有站名
    all_stations = [
    "Songshan",
    "Nanjing Sanmin",
    "Taipei Arena",
    "Nanjing Fuxing",
    "Songjiang Nanjing",
    "Zhongshan",
    "Beimen",
    "Ximen",
    "Xiaonanmen",
    "Chiang Kai-Shek Memorial Hall",
    "Guting",
    "Taipower Building",
    "Gongguan",
    "Wanlong",
    "Jingmei",
    "Dapinglin",
    "Qizhang",
    "Xindian City Hall",
    "Xindian",
    "Xiaobitan",
  ];
    # messages物件的屬性
    # dict.keys()類似於JS中的Object.keys()
    # 但返回類型是dict_keys(僅支援迭代、長度檢查等基本操作，無法修改內容)
    # 如果需要使用list的方法，必須先用 list() 進行轉換
    friends = list(messages.keys());
    # messages物件的值
    # dict.values()類似於JS中的Object.values()
    friends_stations = list(messages.values());
    # currentStation的index
    # list.index()類似於JS中的Array.indexOf()
    my_station = all_stations.index(current_station);
    # currentStation和每個人的距離
    distance = []
    # range 用法：range(start, stop, step)
    # JS 的 for...of 在 Python 中對應為 for...in (遍歷陣列的值)
    # JS 的 for...in 在 Python 中對應為 for...in（遍歷字典的鍵） 或 range()（遍歷陣列的索引）
    for i in range(len(friends_stations)):
        # 每個人所在的station的index
        # enumerate：類似於JS中的forEach/for...in（陣列），同時返回索引和元素
        for index, station in enumerate(all_stations):
            if station in friends_stations[i]:
                station_index = index
                break
        # 計算自己和每個人所在的station的距離(取絕對值)
        # 如果自己/朋友所在的station為"Xiaobitan"，從"Qizhang"出發再算距離
        Xiaobitan = all_stations.index("Xiaobitan");
        Qizhang = all_stations.index("Qizhang");
        if (my_station == Xiaobitan < 18) and (station_index == Xiaobitan):
            distance.append(0)
        elif my_station == Xiaobitan:
            distance.append(abs(station_index - Qizhang) + 1)
        elif station_index == Xiaobitan:
            distance.append(abs(my_station - Qizhang) + 1)
        else:
            distance.append(abs(my_station - station_index))
    # 找出距離最近的朋友
    nearest = distance.index(min(distance));
    # 打印結果
    print(friends[nearest])

messages={
    "Leslie":"I'm at home near Xiaobitan station.",
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Vivian":"I'm at Xindian station waiting for you."
    }
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

print("===Task 2===");
time_table = {
  "John": [],
  "Bob": [],
  "Jenny": [],
};
def book(consultants, hour, duration, criteria):
    # 計算預約時間段
    reservation = [];
    for i in range(hour,hour + duration+1):
        reservation.append(i)
    # 找出與預約時間匹配的顧問
    status = [];
    unavailable = list(time_table.values());
    for arr in unavailable:
        free = True
        for time in reservation:
            if time in arr:
                free = False
                break
        status.append(free)
    
    available=[]
    for i in range(len(status)):
        if status[i] == True:
            available.append(consultants[i])
    # 依照價錢/評價選擇顧問
    consultant=""
    if (len(available)==0):
        print("No Service")
    elif criteria == "price":
        price = []
        for consultant in available:
            price.append(consultant["price"])
        lowest = min(price);
        for i in range(len(available)):
            if(available[i]["price"] == lowest):
                consultant = available[i]["name"];
    else:
        rate = []
        for consultant in available:
            rate.append(consultant["rate"])
        highest = max(rate);
        for i in range(len(available)):
            if(available[i]["rate"] == highest):
                consultant = available[i]["name"];
    # 確定顧問後，更新時間表
    # Python 中合併兩個陣列的方法
    # 1 + 運算符：返回新列表
    # 2 extend()：直接修改原列表
    # 3 解包運算符 *（類似於 JS 的展開運算符 ...）
    if consultant!="":
        time_table[consultant] = [*time_table[consultant], *reservation]
        print(consultant);

consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
    ]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

print("===Task 3===");
def func(*data):
    # 將所有姓名放入數組
    names = [*data];
    # 找出所有名字的中間字
    middle_name = []
    for name in names:
        middle_name.append(name[math.floor(len(name) / 2)])
    # 累計每個中間字出現的次數
    # dict.get(key, default)
    # 檢查鍵是否存在(返回值或預設值)，對應JS的key in obj ? obj[key] : default
    # dict.update(new_dict)
    # 新增或更新物件中的屬性，對應JS的Object.assign(obj, newProperties)
    def update_counts(all_names, name):
        all_names[name] = all_names.get(name, 0) + 1
        return all_names
    counted_names = reduce(update_counts, middle_name, {})
    # 找出只出現 1 次的中間字
    different = "";
    for key in counted_names:
        if counted_names[key] == 1:
            different = key;
    # 依照索引值打印出名字
    if different == "":
        print("沒有");
    else:
        index = ""
        for i,name in enumerate(names):
            if different in name:
                index = i
                break
        print(names[index]);
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

print("===Task 4===");
def get_number(index):
    number = 0;
    # 索引如果是 3 的倍數要減 1，其餘則 +4
    for i in range(1,index+1):
        if (i % 3 == 0):
            number += -1;
        else:
            number += 4;
    print(number);
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

print("===Task 5===");
def find(spaces, stat, n):
    seat = float('inf');
    car = -1;
    for i in range(len(stat)):
    # 找出狀態為 1，且空間比 n 大的車廂
        if stat[i] == 1 and spaces[i] >= n:
        # 如果空間比較小，更新座位數及車廂索引
            if spaces[i] < seat:
                seat = spaces[i];
                car = i;
    print(car);
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2