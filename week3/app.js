const open = document.getElementById("open");
const close = document.getElementById("close");
const load = document.getElementById("load");
const nav = document.querySelector(".mobile");
const promotions = document.querySelector(".promotions");
const titles = document.querySelector(".titles");
let spotTitle = [];
let firstPhoto = [];
let startIndex = 3;
let endIndex = startIndex + 10;

// retrieve data
async function fetchSpots() {
  try {
    let responseObj = await fetch(
      "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
    );
    let json = await responseObj.json();
    return json.data.results;
  } catch (e) {
    window.alert("Something went wrong...Please try again later");
    return [];
  }
}

// 過濾列表資料、渲染HTML元素
async function renderHTML() {
  let spotList = await fetchSpots();
  spotTitle = [...spotList.map((spot) => spot.stitle)];
  let spotPhoto = spotList.map((spot) => spot.filelist);
  firstPhoto = [
    ...spotPhoto.map((photo) => {
      const regex = /https:\/\/.*?\.jpg/i;
      return photo.match(regex)[0];
    }),
  ];
  renderPromotion();
  renderTitle();
  console.log(spotList);
}

//渲染Promotion元素
function renderPromotion() {
  for (let i = 0; i < 3; i++) {
    const li = document.createElement("li");
    const img = document.createElement("img");
    const p = document.createElement("p");

    li.classList = i === 2 ? "promotion last" : "promotion";
    img.src = firstPhoto[i];
    img.alt = spotTitle[i];
    p.innerText = spotTitle[i];

    li.appendChild(img);
    li.appendChild(p);
    promotions.appendChild(li);
  }
}

//渲染Title元素
function renderTitle() {
  for (let i = startIndex; i < endIndex; i++) {
    const li = document.createElement("li");
    const star = document.createElement("button");
    const starImg = document.createElement("img");
    const img = document.createElement("img");
    const p = document.createElement("p");

    if (i % 10 === 3 || i % 10 === 8) {
      li.classList = "wide-img";
    }
    if (i % 10 === 1 || i % 10 === 2) {
      li.classList = "last";
    }

    star.type = "button";
    star.classList = "star";
    starImg.src = "./images/star_icon.png";
    starImg.alt = "star";
    star.addEventListener("click", (e) => toggleStar(e));
    img.classList = "photos";
    img.src = firstPhoto[i];
    img.alt = spotTitle[i];
    p.classList = "title";
    p.innerText = spotTitle[i];

    star.appendChild(starImg);
    li.appendChild(star);
    li.appendChild(img);
    li.appendChild(p);
    titles.appendChild(li);
  }
}

// 點擊按鈕加載更多
function loadMore() {
  startIndex = startIndex + 10;
  endIndex = startIndex + 10;
  if (endIndex > spotTitle.length) {
    endIndex = spotTitle.length;
    load.style.display = "none";
  }
  renderTitle();
}

// 根據點擊的按紐，開啟/關閉側邊欄
function toggleMenu(e) {
  const currentMode = e.currentTarget.id;
  if (currentMode === "close") {
    nav.style.display = "none";
  }
  if (currentMode === "open") {
    nav.style.display = "flex";
  }
}

// 若視窗大小超過600px，關閉側邊欄
function handleResize() {
  const width = window.innerWidth;
  if (width > 600) {
    nav.style.display = "none";
  }
}

// 點擊星星可加入最愛
function toggleStar(e) {
  const currentStar = e.currentTarget;
  currentStar.classList.toggle("active");
}

open.addEventListener("click", (e) => toggleMenu(e));
close.addEventListener("click", (e) => toggleMenu(e));
load.addEventListener("click", (e) => loadMore(e));
window.addEventListener("resize", handleResize);
renderHTML();
