const burgerNav = document.querySelector(".burger");
const navBar = document.querySelector("nav");
const navList = document.querySelector(".nav-list");
const navLinks = document.querySelectorAll(".nav-list li");
const body = document.querySelectorAll("section");

// MANAGEMENT PAGE
const updateBrooder = document.querySelectorAll(".update-brooder");



try {
  burgerNav.addEventListener("click", () => {
    navBar.classList.toggle("nav-active");
    navList.classList.toggle("nav-list-active");
    if (navBar.classList.value == "nav-active") {
      navLinks.forEach((link) => {
        link.addEventListener("click", resizeNav);
      });
      body.forEach((section) => {
        section.addEventListener("click", resizeNav);
      });
    }
  });
} catch (error) {
  console.log("NavBar Element not found in current page: ", error);
}

function resizeNav() {
  navBar.classList.remove("nav-active");
  navList.classList.remove("nav-list-active");
}
