let shops = document.getElementById("shops-count");
let shopsLabel = document.getElementById("shops-count-label");
let shopsLabelTotal = document.getElementById("shops-total");
let months = document.getElementById("months");
let monthsLabel = document.getElementById("months-label");
let monthsLabelTotal = document.getElementById("months-total");
let currentPrice = document.getElementById("checkout");
let radioTrigger = document.querySelectorAll('input[type=radio][name="plan-type"]');

Array.prototype.forEach.call(radioTrigger, function (radio) {
    radio.addEventListener('change', count);
});


function count() {
    let preTotal = document.querySelector('input[name="plan-type"]:checked');
    let total = parseInt(preTotal.value);
    let shops = parseInt(shopsLabel.innerHTML);
    let months = parseInt(monthsLabel.innerHTML);

    total = total*months;

    if (shops>1){
        total = total + (shops-1)*2990;
    }
    if (months === 12){
        total = total * 0.75;
    }
    else if (months >= 6){
        total *= 0.85;
    }
    currentPrice.innerHTML = total;
}

shops.addEventListener("input", function (event) {
    shopsLabel.innerHTML = event.currentTarget.value;
    shopsLabelTotal.innerHTML = event.currentTarget.value;

    if (event.currentTarget.value === '1') {
        shopsLabelTotal.innerHTML += " доп. магазин";
    }
    else {
        if ((1 < event.currentTarget.value) & (event.currentTarget.value < 5)) {
            shopsLabelTotal.innerHTML += " доп. магазина";
        }
        else {
            shopsLabelTotal.innerHTML += " доп. магазинов";
        }
    }
    count();
});

months.addEventListener("input", function (event) {
    let monthsVal = document.getElementById("months").value;
    monthsLabel.innerHTML = monthsVal;
    monthsLabelTotal.innerHTML = monthsVal;
    if (event.currentTarget.value === '1') {
        monthsLabelTotal.innerHTML += " месяц";
    }
    else {
        if ((1 < event.currentTarget.value) & (event.currentTarget.value < 5)) {
            monthsLabelTotal.innerHTML += " месяца";
        }
        else {
            monthsLabelTotal.innerHTML += " месяцев";
        }
    }
    count();
});


