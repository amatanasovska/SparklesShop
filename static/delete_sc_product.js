function delete_sc_product(id)
{
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET","/delete_sc_product?id=" + id );
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
    
}