// Dom Elements
const adminLinks = document.querySelectorAll(".admin-func");

console.log(adminLinks);

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
  //   console.log("Session Activate:", section);
  switch (linkName) {
    case "flock":
      section.classList.add("active-panel");
      break;
    case "brooders":
      section.classList.add("active-panel");
      break;
    case "orders":
      return section.classList.add("active-panel");
      break;
    case "feedback":
      return section.classList.add("active-panel");
      break;
    case "location":
      return section.classList.add("active-panel");
      break;
    case "statistics":
      return section.classList.add("active-panel");
      break;
    default:
      return section.classList.add("active-panel");
      break;
  }
};
