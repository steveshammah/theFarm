try {
  const editProfile = document.querySelectorAll(".edit-profile");
  const userInfo = document.querySelector(".user-info");
  const profileSettings = document.querySelector(".profile-settings");
  const orderButton = document.querySelectorAll(".order-form .btn");
  const username = document.querySelector("#username").innerHTML;
  const checkout = document.querySelector(".checkout");

  editProfile.forEach((button) => {
    button.addEventListener("click", (e) => {
      switch (e.target.innerHTML) {
        case "Edit":
          userInfo.style.display = "none";
          profileSettings.style.display = "flex";
          break;
        case "Cancel":
          profileSettings.style.display = "none";
          userInfo.style.display = "flex";
          break;
        default:
          userInfo.style.display = "flex";
          break;
      }
    });
  });

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

      // console.log("PRODUCT: ", product);
      const order = { product: product, quantity: quantity };
      // console.log("SAVING ORDERS: ", order);
      saveOrders(username, order);

      parentElement.childNodes[1].value = "";
    });
  });

  function checkOrders(username) {
    //CHECK IF IN STORAGE
    let orders;
    if (localStorage.getItem(username) == null) {
      orders = [];
      // console.log("NO ORDERS FOUND");
    } else {
      orders = JSON.parse(localStorage.getItem(username));
      // console.log("ORDERS: ", orders);
      return true;
    }
  }

  function saveOrders(username, order) {
    let orders;
    if (checkOrders(username)) {
      orders = JSON.parse(localStorage.getItem(username));
      // console.log("SAVING ORDERS NEW FUNC: ", orders);
      for (let i = 0; i < orders.length; i++) {
        // console.log(orders[i].product === orderList.product);
        if (orders[i].product == order.product) {
          // console.log("IF EXECUTING", orders[i]);
          orders[i] = order;
          // console.log(orders[i]);
          localStorage.setItem(username, JSON.stringify(orders));
        } else {
          orders.push(order);
          // console.log("ELSE EXECUTING!!", orders);
          // localStorage.setItem(username, JSON.stringify(orders));
        }
      }
    } else {
      orders = [];
      orders.push(order);
      // console.log("EXECUTING!!", orders);
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

    const userOrders = JSON.parse(localStorage.getItem(username));

    const fetchOrders = [
      ...new Map(userOrders.map((order) => [order.product, order])).values(),
    ];

    const broilers = Number(
      fetchOrders.filter((order) => order.product == "broilers")[0].quantity
    );
    console.log("Broilers: ", broilers);
    const layers = Number(
      fetchOrders.filter((order) => order.product == "layers")[0].quantity
    );

    const chicks = Number(
      fetchOrders.filter((order) => order.product == "chicks")[0].quantity
    );

    const quantitySum = layers + broilers + chicks;
    const costSum = layers * 400 + broilers * 600 + chicks * 70;
    totatCost.innerText = costSum;
    totalQuantity.innerHTML = quantitySum;
    layersOrders.value = layers;
    layersAmount.innerText = layers * 400;
    broilersOrders.value = broilers;
    broilersAmount.innerText = broilers * 600;
    chicksOrders.value = chicks;
    chicksAmount.innerText = chicks * 70;
  };

  updateOrders();

  checkout.addEventListener("click", () => {
    if (checkOrders(username)) {
      localStorage.removeItem(username);
    }
  });
} catch (error) {
  console.log(error);
}
