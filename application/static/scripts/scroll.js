let item = document.getElementById("scroll-hook");

item.addEventListener("wheel", function (target) {
    item.scrollLeft += target.deltaY*5;
})
