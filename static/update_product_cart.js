function updateValue(event,index)
{
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "update_shopping_cart?id=" + index + "&qty=" + event.currentTarget.value);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
    
    var i =0;
    var total = 0;
    while(true){
        var price = document.getElementById(i+"_price")
        if(price)
        {
            price = price.innerHTML
            let qty = document.getElementById(i+"_qty").value
            console.log(price)
            console.log(qty)
            total += parseInt(price)*parseInt(qty)
            
        }
        else
        {
            break;
        }
        i+=1
    }
    var price_span = document.getElementById("total_price")
    price_span.innerHTML = total

}
