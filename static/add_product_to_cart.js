

function addToCart(qty, id) {
    let shopping_cart_items_number = document.getElementById("shopping_cart_items_number");
    let number = parseInt(shopping_cart_items_number.innerHTML) + 1
    console.log(number)
    shopping_cart_items_number.innerHTML = number

    qty=1

    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/add_to_cart?id=" + id + "&qty=" + qty);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

