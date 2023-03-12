
function event_control(){
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const location = document.getElementById("location").value;
    const ticket_price = document.getElementById("ticket_price").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    console.log(name)

    if(name == "" || description == "" || location == "" || ticket_price == "" || date == ""|| time == ""){
        document.getElementById("error").innerHTML = "All input fields must be filled";
    }

    else
        document.getElementById("regbtn").click();

}
