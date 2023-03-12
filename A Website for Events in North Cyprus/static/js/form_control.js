const name = document.getElementById("username");
console.log(username)

function form_control(){
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const firstname = document.getElementById("firstname").value;
    const lastname = document.getElementById("lastname").value;
    const email = document.getElementById("email").value;
    let checkUpper = 0;
    let checkLower = 0;
    let checkDigit = 0;


    for(let i=0; i<password.length; ++i){
        if(!isNaN(parseInt(password[i])))
            checkDigit = 1;
        if(isNaN(parseInt(password[i])) && password[i] == password[i].toLowerCase())
            checkLower = 1;
        if(isNaN(parseInt(password[i])) && password[i] == password[i].toUpperCase())
            checkUpper = 1;
    }

    if(username == "" || password == "" || firstname == "" || lastname == "" || email == ""){
        document.getElementById("error").innerHTML = "All input fields must be filled";
    }
    else if(document.getElementById("username").value.toLowerCase() == document.getElementById("txtHint").innerText.toLowerCase()){
        document.getElementById("error").innerHTML = "Please enter a unique username";
    }
    else if(password.length<8){
        document.getElementById("error").innerHTML = "Password must be longer than 8";
    }
    else if(checkDigit == 0){
        document.getElementById("error").innerHTML = "Password must contain a digit";
    }
    else if(checkUpper == 0){
        document.getElementById("error").innerHTML = "Password must contain an uppercase letter";
    }
    else if(checkLower == 0 ){
        document.getElementById("error").innerHTML = "Password must contain a lowercase letter";
    }
    else
        document.getElementById("regbtn").click();

}


function showHint(str){
            if(str.length == 0){
                document.getElementById("txtHint").innerHTML = "";
                return;
            }
            else {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function(){
                    if(this.readyState == 4 && this.status == 200){
                        document.getElementById("txtHint").innerHTML = this.responseText;
                    }
                };
                xmlhttp.open("GET", "/listexistinguser?q=" + str, true);
                xmlhttp.send();
            }
        }