const orderButton = document.querySelectorAll(".order-form .btn");
const username = document.querySelector("#username").innerHTML;

orderButton.forEach((button) => {
  button.addEventListener("click", (e) => {
    const parentElement = button.parentElement;
    e.preventDefault();
    // console.log("Parent Element", parentElement.childNodes[1]);
    const product = parentElement.id;
    const quantity = parentElement.childNodes[1].value;
    const productSpan = document.querySelector(`.${product} .order-success`);
    productSpan.style.display = "block";

    setTimeout(() => {
      productSpan.style.display = "none";
    }, 5000);
    checkOrders(username);

    console.log("PRODUCT: ", product);
    const order = { product, quantity };
    console.log("SAVING ORDERS: ", order);
    saveOrders(order);

    parentElement.childNodes[1].value = "";
  });
});

function checkOrders(username) {
  //CHECK IF IN STORAGE
  let orders;
  if (localStorage.getItem(username) == null) {
    orders = [];
    console.log("NO ORDERS FOUND");
  } else {
    orders = JSON.parse(localStorage.getItem(username));
    // console.log("ORDERS: ", orders);
    return true;
  }
}

function saveOrders(orderList) {
  let orders;
  if (checkOrders(username)) {
    orders = JSON.parse(localStorage.getItem(username));
    console.log("SAVING ORDERS NEW FUNC: ", orders);
    for (let i = 0; i < orders.length; i++) {
      console.log(orders[i].product === orderList.product);
      if (orders[i].product === orderList.product) {
        console.log("IF EXECUTING");
        orders[i] = orderList;
        localStorage.setItem(username, JSON.stringify(orders));
      } else {
        orders.push(orderList);
        console.log("ELSE EXECUTING!!");
        localStorage.setItem(username, JSON.stringify(orders));
      }
    }
  } else {
    orders = [];
    orders.push(orderList);
    console.log("EXECUTING!!");
    localStorage.setItem(username, JSON.stringify(orders));
  }
  updateOrders();
}

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

  // console.log("Username:, ", username);
  // console.log(localStorage.getItem("janedoe"));
  // const userOrders = JSON.parse(localStorage.getItem(username));
  // console.log("USER ORDERS: ", userOrders);
  // const layers = Number(userOrders.products.layers);
  // const broilers = userOrders.quantity;
  // const chicks = Number(userOrders.products.chicks);
  // console.log("Broilers: ", broilers);
  // const quantitySum = layers + broilers + chicks;
  // console.log(layersOrders);
  // totatCost.innerText = costSum;
  // totalQuantity.innerText = quantitySum;
  // layersOrders.innerText = layers;
  // layersAmount.innerText = layers * 400;
  // broilersOrders.innerText = broilers;
  // broilersAmount.innerText = broilers * 600;
  // chicksOrders.innerText = chicks;
  // chicksAmount.innerText = chicks * 70;
};

updateOrders();
