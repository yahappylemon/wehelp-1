console.log("===Task 1===");
function findAndPrint(messages, currentStation) {
  // 所有站名
  const allStations = [
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

  // messages物件的屬性
  const friends = Object.keys(messages);
  // messages物件的值
  const friendsStations = Object.values(messages);
  // currentStation的index
  const myStation = allStations.indexOf(currentStation);
  // currentStation和每個人的距離
  const distance = [];

  for (let i = 0; i < friendsStations.length; i++) {
    // 每個人所在的station的index
    const stationIndex = allStations.findIndex((station) =>
      friendsStations[i].includes(station)
    );
    // 計算自己和每個人所在的station的距離(取絕對值)
    // 如果自己/朋友所在的station為"Xiaobitan"，從"Qizhang"出發再算距離
    const Xiaobitan = allStations.indexOf("Xiaobitan");
    const Qizhang = allStations.indexOf("Qizhang");
    if (myStation === Xiaobitan && stationIndex === Xiaobitan) {
      distance.push(0);
    } else if (myStation === Xiaobitan) {
      distance.push(Math.abs(stationIndex - Qizhang) + 1);
    } else if (stationIndex === Xiaobitan) {
      distance.push(Math.abs(myStation - Qizhang) + 1);
    } else {
      distance.push(Math.abs(myStation - stationIndex));
    }
  }
  //找出距離最近的朋友
  const nearest = distance.indexOf(Math.min(...distance));
  // 打印結果
  console.log(friends[nearest]);
}
const messages = {
  Bob: "I'm at Ximen MRT station.",
  Mary: "I have a drink near Jingmei MRT station.",
  Copper: "I just saw a concert at Taipei Arena.",
  Leslie: "I'm at home near Xiaobitan station.",
  Vivian: "I'm at Xindian station waiting for you.",
};
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian
findAndPrint(messages, "Xiaobitan"); // print Leslie

console.log("===Task 2===");
let timeTable = {
  John: [],
  Bob: [],
  Jenny: [],
};
function book(consultants, hour, duration, criteria) {
  // 計算預約時間段
  let reservation = [];
  for (let i = hour; i <= hour + duration; i++) {
    reservation.push(i);
  }
  // 找出與預約時間匹配的顧問
  let status = [];
  let unavailable = Object.values(timeTable);
  for (let i = 0; i < unavailable.length; i++) {
    status = unavailable.map((arr) => {
      for (const time of reservation) {
        if (arr.includes(time)) {
          return false;
        }
      }
      return true;
    });
  }
  const available = consultants.filter(
    (consultant, index) => status[index] === true
  );
  // 依照價錢/評價選擇顧問
  let consultant;
  if (available.length === 0) {
    console.log("No Service");
  }
  if (criteria === "price") {
    const price = available.map((consultant) => consultant.price);
    const lowest = Math.min(...price);
    for (let key in available) {
      if (available[key].price === lowest) {
        consultant = available[key].name;
      }
    }
  }
  if (criteria === "rate") {
    const rate = available.map((consultant) => consultant.rate);
    const highest = Math.max(...rate);
    for (let key in available) {
      if (available[key].rate === highest) {
        consultant = available[key].name;
      }
    }
  }
  // 確定顧問後，更新時間表
  if (consultant) {
    timeTable[consultant] = [...timeTable[consultant], ...reservation];
    console.log(consultant);
  }
}
const consultants = [
  { name: "John", rate: 4.5, price: 1000 },
  { name: "Bob", rate: 3, price: 1200 },
  { name: "Jenny", rate: 3.8, price: 800 },
];
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John

console.log("===Task 3===");
function func(...data) {
  // 將所有姓名放入數組
  const names = [...data];
  // 找出所有名字的中間字
  const middleName = names.map((name) => name[Math.floor(name.length / 2)]);
  // 累計每個中間字出現的次數
  const countedNames = middleName.reduce((allNames, name) => {
    name in allNames ? allNames[name]++ : (allNames[name] = 1);
    return allNames;
  }, {});
  // 找出只出現 1 次的中間字
  let different = "";
  for (let key in countedNames) {
    if (countedNames[key] === 1) {
      different = key;
    }
  }
  //依照索引值打印出名字
  if (different === "") {
    console.log("沒有");
  } else {
    let index = names.findIndex((name) => name.includes(different));
    console.log(names[index]);
  }
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安

console.log("===Task 4===");
function getNumber(index) {
  let number = 0;
  // 索引如果是 3 的倍數要減 1，其餘則 +4
  for (let i = 1; i <= index; i++) {
    if (i % 3 === 0) {
      number += -1;
    } else {
      number += 4;
    }
  }
  console.log(number);
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70

console.log("===Task 5===");
function find(spaces, stat, n) {
  let seat = Infinity;
  let car = -1;
  for (let i = 0; i < stat.length; i++) {
    // 找出狀態為 1，且空間比 n 大的車廂
    if (stat[i] === 1 && spaces[i] >= n) {
      // 如果空間比較小，更新座位數及車廂索引
      if (spaces[i] < seat) {
        seat = spaces[i];
        car = i;
      }
    }
  }
  console.log(car);
}
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2); // print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
