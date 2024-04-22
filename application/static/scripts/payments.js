let shops = document.getElementById("shops-count");
let shopsLabel = document.getElementById("shops-count-label");
let months = document.getElementById("months");
let monthsLabel = document.getElementById("months-label");

shops.addEventListener("input", function(event){
    shopsLabel.innerHTML = event.currentTarget.value;
});

months.addEventListener("input", function(event){
    let monthsVal = document.getElementById("months").value;
    monthsLabel.innerHTML = monthsVal;
});