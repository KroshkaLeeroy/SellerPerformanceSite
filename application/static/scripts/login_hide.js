let eye = document.getElementById("hide-password");
let field = document.getElementById("login-password");

eye.onclick = function(){
    if (field.type == "password"){
        field.type = "text";
    }
    else{
        field.type = "password";
    }
}