const orderButton = document.querySelectorAll(".order-form .btn");
console.log(orderButton);

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
    console.log("SAVING ORDERS");

    storeOrder(product, quantity);
    parentElement.childNodes[1].value = "";
    console.log(order);
  });
});

const storeOrder = (product, quantity) => {
  localStorage.setItem(product, quantity);
  updateOrders();
  return true;
};

const updateOrders = () => {
  const layers = localStorage.getItem("layers");
  const broilers = localStorage.getItem("broilers");
  const chicks = localStorage.getItem("chicks");
  const costSum = layers + broilers + chicks;
  const quantitySum = Number(layers) + Number(broilers) + Number(chicks);

  // Dom Elements to update
  const layersOrders = document.querySelector(".layers-orders");
  const broilersOrders = document.querySelector(".broilers-orders");
  const chicksOrders = document.querySelector(".chicks-orders");
  const totatCost = document.querySelector(".total-cost");
  const totalQuantity = document.querySelector(".total-quantity");

  // console.log(layersOrders);
  totatCost.innerText = costSum;
  totalQuantity.innerText = quantitySum;
  layersOrders.innerText = layers;
  broilersOrders.innerText = broilers;
  chicksOrders.innerText = chicks;
};

updateOrders();
