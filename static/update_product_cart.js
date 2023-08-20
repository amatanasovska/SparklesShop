function updateValue(event,index)
{
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "update_shopping_cart?id=" + index + "&qty=" + event.currentTarget.value);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
    

}
  