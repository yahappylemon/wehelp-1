const box = document.getElementById("checkbox");
const loginForm = document.getElementById("login");
const square = document.getElementById("square");
const mathForm = document.getElementById("math");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  if (box.checked) {
    return loginForm.submit();
  }
  alert("Please check the checkbox first");
});

mathForm.addEventListener("click", (e) => {
  const value = Number(square.value);
  if (value <= 0 || value === "") {
    alert("Please enter a positive number");
  } else {
    window.location.href = `/square/${value}`;
  }
});
