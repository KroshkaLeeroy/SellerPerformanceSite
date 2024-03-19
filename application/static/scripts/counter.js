let text = document.getElementById("question");
let counterDiv = document.getElementById("counter");

text.addEventListener("input", function(target){
    counterDiv.innerHTML = (text.value.length + "/400");
    if (text.value.length >400){
        text.value = text.value.slice(0, 400);
        counterDiv.innerHTML = (text.value.length + "/400");
        alert("Вы превысили допустимый лимит вводимых символов!");
    }
});