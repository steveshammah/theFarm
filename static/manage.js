// Dom Elements
const adminLinks = document.querySelectorAll(".admin-func");

// console.log(adminLinks);

// Event Listeners
adminLinks.forEach((link) => {
  return link.addEventListener("click", (event) => {
    const link = event.target;
    const linkName = event.target.innerHTML.toLowerCase();
    removeActiveClass();
    link.classList.add("active-func");
    activateStatContainer(linkName);
  });
});

// Remove Active Class
const removeActiveClass = () => {
  const adminList = document.querySelectorAll(".admin-panel section");
  adminList.forEach((listItem) => (listItem.className = "hidden-panel"));
  adminLinks.forEach((link) => link.classList.remove("active-func"));
};

// Add Active Panel Class
const activateStatContainer = (linkName) => {
  const section = document.getElementById(`${linkName}`);
  section.classList.add("active-panel");
};
