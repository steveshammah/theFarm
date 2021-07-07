const userDetails = {
    _username : ' ' ,
    _email : ' ' ,
    _userId : ' ' ,
    _orders : {
        chicks: ' ',
        layers: ' ',
        broilers: ' ',
    },

    get username() {
        return this._username;
    },
    get email() {
        return this._email;
    },
    get userId() {
        return this._userId;
    },
    get orders() {
        return this._orders;
    },

    set username(newName) {
        this._username = newName;
    },
    set email(newEmail) {
        this._email = newEmail;
    },
    set userId(newUserId) {
        this._userId = newUserId;
    },
    set orders(ordersObj) {                    //object as param
        this._orders = ordersObj;
    },
}


const userName = document.querySelector('#username');
const email = document.querySelector('#email');
const userId = document.querySelector('#user-id');
const orders = document.querySelector('#order-list');



console.log(userName, email, userId, orders)
userDetails.username = userName.innerHTML;
userDetails.email = email.innerHTML;
userDetails.userId = userId.innerHTML;
userDetails.orders = orders.innerHTML;


console.log(userDetails)
