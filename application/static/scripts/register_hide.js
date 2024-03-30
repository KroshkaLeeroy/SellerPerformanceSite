let eye1 = document.getElementById("hide-password1");
let eye2 = document.getElementById("hide-password2");
let field1 = document.getElementById("password");
let field2 = document.getElementById("password-repeat");

eye1.onclick = function(){
    if (field1.type == "password"){
        field1.type = "text";
    }
    else{
        field1.type = "password";
    }
}

eye2.onclick = function(){
    if (field2.type == "password"){
        field2.type = "text";
    }
    else{
        field2.type = "password";
    }
}