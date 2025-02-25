const signup = document.getElementById("signup");
const login = document.getElementById("login");
const chat = document.getElementById("chat");
const deleteMessage = document.getElementById("deleteMessage");
const searchName = document.getElementById("searchName");
const member = document.getElementById("member");
const updateName = document.getElementById("updateName");
const result = document.getElementById("result");

async function generalFetch(url, options) {
  try {
    let response = options ? await fetch(url, options) : await fetch(url);
    let data = await response.json();
    return data;
  } catch (error) {
    window.alert("Something went wrong:" + error.message);
    throw error;
  }
}

async function searchAccount(e) {
  e.preventDefault();
  const form = e.currentTarget;
  const formData = new FormData(form);
  const username = formData.get("username").trim();
  if (username === "") {
    window.alert("Please enter a value");
    return;
  }
  let data = await generalFetch(
    `http://127.0.0.1:8000/api/member?username=${encodeURIComponent(username)}`
  );
  data.data === null
    ? (member.innerText = "No Data")
    : (member.innerText = `${data.data.name}(${data.data.username})`);
}

async function updateAccount(e) {
  e.preventDefault();
  const form = e.currentTarget;
  const formData = new FormData(form);
  const newName = formData.get("newName").trim();
  if (newName === "") {
    window.alert("Please enter a value");
    return;
  }
  let data = await generalFetch("http://127.0.0.1:8000/api/member", {
    method: "PATCH",
    body: JSON.stringify({ name: newName }),
    headers: { "Content-Type": "application/json" },
  });
  data.ok ? (result.innerText = "更新成功") : (result.innerText = "更新失敗");
}

function emptyInput(e) {
  e.preventDefault();
  const form = e.currentTarget;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  const value = Object.values(data);
  for (let input of value) {
    if (input.trim() === "") {
      window.alert("Please enter a value");
      return;
    }
  }
  form.submit();
}

function confirmDelete(e) {
  e.preventDefault();
  if (window.confirm("Do you really want to delete?")) {
    e.currentTarget.submit();
  }
}

if (signup) {
  signup.addEventListener("submit", (e) => emptyInput(e));
}
if (login) {
  login.addEventListener("submit", (e) => emptyInput(e));
}
if (chat) {
  chat.addEventListener("submit", (e) => emptyInput(e));
}
if (deleteMessage) {
  deleteMessage.addEventListener("submit", (e) => confirmDelete(e));
}
if (searchName) {
  searchName.addEventListener("submit", (e) => searchAccount(e));
}
if (updateName) {
  updateName.addEventListener("submit", (e) => updateAccount(e));
}
