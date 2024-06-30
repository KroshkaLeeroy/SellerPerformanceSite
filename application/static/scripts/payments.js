let shops = document.getElementById("shops-pick");
let shopsSub = document.getElementById("shops-node-label");
let shopsLabel = document.getElementById("shops-node");
let shopsLabelTotal = document.getElementById("shops-total");
let months = document.getElementById("months-pick");
let monthsSub = document.getElementById("months-node-label");
let monthsLabel = document.getElementById("months-node");
let monthsLabelTotal = document.getElementById("months-total");
let currentPrice = document.getElementById("checkout");
let radioTrigger = document.querySelectorAll('input[type=radio][name="plan-type"]');
let planLabel = document.getElementById("chosen-plan");
let startChose = document.getElementById("start-chose");
let businessChose = document.getElementById("business-chose");



Array.prototype.forEach.call(radioTrigger, function (radio) {
    radio.addEventListener('change', count);
});


function count() {
    let preTotal = parseInt(document.querySelector('input[name="plan-type"]:checked').value);
    let total = preTotal;
    let shops = parseInt(shopsLabel.innerHTML);
    let months = parseInt(monthsLabel.innerHTML);

    total = total * months;

    if (shops > 1) {
        total = total + (shops - 1) * preTotal;
    }
    if (months === 12) {
        total = total * 0.75;
    }
    else if (months >= 6) {
        total *= 0.85;
    }
    currentPrice.innerHTML = total;
    if (preTotal == 3990) {
        startChose.innerHTML = "<img src='/static/images/check.svg'>Выбрано"
        businessChose.innerHTML = "Выбрать"
        planLabel.innerHTML = "Тариф Старт"
    }
    else {
        startChose.innerHTML = "Выбрать"
        businessChose.innerHTML = "<img src='/static/images/check.svg'>Выбрано"
        planLabel.innerHTML = "Тариф Бизнес"
    }
    document.querySelector('input[name="plan-type"]').parentElement.style.backgroundColor = "#F6F7F9";
    document.querySelector('input[name="plan-type"]').parentElement.style.border = "none";
    document.querySelector('input[name="plan-type"]:checked').parentElement.style.backgroundColor = "white";
    document.querySelector('input[name="plan-type"]:checked').parentElement.style.border = "2px solid #F6F7F9";
}

shops.addEventListener("input", function (event) {
    shopsLabelTotal.innerHTML = event.currentTarget.value;

    if (event.currentTarget.value === '1') {
        shopsLabelTotal.innerHTML += " доп. магазин";
        shopsSub.innerHTML = " магазин";
    }
    else {
        if ((1 < event.currentTarget.value) & (event.currentTarget.value < 5)) {
            shopsLabelTotal.innerHTML += " доп. магазина";
            shopsSub.innerHTML = " магазина";
        }
        else {
            shopsLabelTotal.innerHTML += " доп. магазинов";
            shopsSub.innerHTML = " магазинов";
        }
    }
    shopsLabel.innerHTML = event.currentTarget.value;
    count();
});

months.addEventListener("input", function (event) {
    let monthsVal = document.getElementById("months-pick").value;
    monthsLabelTotal.innerHTML = monthsVal;
    if (event.currentTarget.value === '1') {
        monthsLabelTotal.innerHTML += " месяц";
        monthsSub.innerHTML = " месяц";
    }
    else {
        if ((1 < event.currentTarget.value) & (event.currentTarget.value < 5)) {
            monthsLabelTotal.innerHTML += " месяца";
            monthsSub.innerHTML = " месяца";
        }
        else {
            monthsLabelTotal.innerHTML += " месяцев";
            monthsSub.innerHTML = " месяцев";
        }
    }
    monthsLabel.innerHTML = document.getElementById("months-pick").value;
    count();
});


