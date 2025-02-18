const signup = document.getElementById("signup");
const login = document.getElementById("login");
const chat = document.getElementById("chat");
const deleteMessage = document.getElementById("deleteMessage");

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
