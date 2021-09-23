const orderButton = document.querySelectorAll(".order-form .btn");
console.log(orderButton);

let order = {};

orderButton.forEach((button) => {
  button.addEventListener("click", (e) => {
    const parentElement = button.parentElement;
    e.preventDefault();
    console.log("Parent Element", parentElement.childNodes[1]);
    const product = parentElement.id;
    const quantity = parentElement.childNodes[1].value;
    console.log("Button", button);
    const productSpan = document.querySelector(`.${product} .order-success`);
    productSpan.style.display = "block";

    setTimeout(() => {
      productSpan.style.display = "none";
      console.log(productSpan);
    }, 4000);
    const order = [product, quantity];
    storeOrder(product, quantity);
    parentElement.childNodes[1].value = "";
    console.log(order);
  });
});

const storeOrder = (product, quantity) => {
  localStorage.setItem(product, quantity);
  const layers = localStorage.getItem("layers");
  const broilers = localStorage.getItem("broilers");
  const chicks = localStorage.getItem("chicks");
  console.log("Chicks: ", chicks);
  console.log("Broilers: ", broilers);
  console.log("Layers: ", layers);
  return true;
};
