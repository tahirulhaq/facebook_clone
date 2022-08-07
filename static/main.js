let form = document.querySelector("form"),
  username = document.querySelector(".username"),
  text = document.querySelector(".text"),
  password = document.querySelector(".password");

//console.log(email);
// console.log(error);
// console.log(password);
// console.log(subm);

form.addEventListener("submit", (e) => {
  e.preventDefault();

  //   let pattern = /^[^a-z]{6}@[gmail]\.com /;

  form.classList.add("error");
  form.classList.remove("valid");

});