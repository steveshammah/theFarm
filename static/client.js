const orderButton = document.querySelectorAll(".order-form .btn");
const username = document.querySelector("#username").innerHTML;

console.log(orderButton);

orderButton.forEach((button) => {
  button.addEventListener("click", (e) => {
    const parentElement = button.parentElement;
    e.preventDefault();
    // console.log("Parent Element", parentElement.childNodes[1]);
    const product = parentElement.id;
    const quantity = parentElement.childNodes[1].value;
    console.log("USERNAME: ", username);

    // console.log("Button", button);
    const productSpan = document.querySelector(`.${product} .order-success`);
    productSpan.style.display = "block";

    setTimeout(() => {
      productSpan.style.display = "none";
      console.log(productSpan);
    }, 4000);
    const order = { product, quantity };
    console.log("SAVING ORDERS");

    parentElement.childNodes[1].value = "";
    storeOrder(username, order);
    console.log("username: ", username, "Order: ", order);
  });
});

const storeOrder = (username, order) => {
  localStorage.setItem(username, JSON.stringify(order));
  updateOrders();
  return true;
};

const updateOrders = () => {
  // Dom Elements to update
  const layersOrders = document.querySelector(".layers-orders");
  const layersAmount = document.querySelector(".layers-amount");
  const broilersOrders = document.querySelector(".broilers-orders");
  const broilersAmount = document.querySelector(".broilers-amount");
  const chicksOrders = document.querySelector(".chicks-orders");
  const chicksAmount = document.querySelector(".chicks-amount");
  const totatCost = document.querySelector(".total-cost");
  const totalQuantity = document.querySelector(".total-quantity");

  const userOrders = localStorage.getItem(username);
  console.log("USER ORDERS: ", userOrders);
  // const layers = Number(userOrders.products.layers);
  const broilers = Number(userOrders.products.broilers);
  // const chicks = Number(userOrders.products.chicks);
  console.log("Layers: ", layers);
  // const quantitySum = layers + broilers + chicks;

  // console.log(layersOrders);
  // totatCost.innerText = costSum;
  // totalQuantity.innerText = quantitySum;
  // layersOrders.innerText = layers;
  // layersAmount.innerText = layers * 400;
  broilersOrders.innerText = broilers;
  broilersAmount.innerText = broilers * 600;
  // chicksOrders.innerText = chicks;
  // chicksAmount.innerText = chicks * 70;
};

updateOrders();
