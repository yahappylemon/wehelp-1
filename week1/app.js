const open = document.getElementById("open");
const close = document.getElementById("close");
const nav = document.querySelector(".mobile");
const stars = document.querySelectorAll(".star");

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
  const currentStar = e.target;
  currentStar.classList.toggle("active");
}

open.addEventListener("click", (e) => toggleMenu(e));
close.addEventListener("click", (e) => toggleMenu(e));
stars.forEach((star) => star.addEventListener("click", (e) => toggleStar(e)));
window.addEventListener("resize", handleResize);
