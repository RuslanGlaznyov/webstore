window.onload=function(){

    var images = document.querySelectorAll("#slider .images .slide");
    var prev = document.querySelector("#slider .contr-slider .prev");
    var next = document.querySelector("#slider .contr-slider .next");
    var dots = document.querySelectorAll("ul li .dot");
    var carrent_img = 0;

    not_active_color = "#D6D6D6";
    active_color = "#869791";
    dots[carrent_img].style.backgroundColor = active_color;


    next.onclick = next_img;
    function next_img(){
        images[carrent_img].classList.remove("show");
        dots[carrent_img].style.backgroundColor = not_active_color;
        carrent_img++;
        if(carrent_img >= images.length){
            carrent_img = 0
        }
        images[carrent_img].classList.add("show");
        dots[carrent_img].style.backgroundColor = active_color;
    }

    prev.onclick = prev_img;
    function prev_img(){

        images[carrent_img].classList.remove("show");
        dots[carrent_img].style.backgroundColor = not_active_color;
        carrent_img--;
        if(carrent_img < 0 ){
            carrent_img = images.length-1;
        }
        images[carrent_img].classList.add("show");

        dots[carrent_img].style.backgroundColor = active_color;
    }

    for(var j = 0; j < dots.length; j++ ){
        (function(j){
            dots[j].addEventListener('click',function(){
                dots[carrent_img].style.backgroundColor = not_active_color;
                dots[j].style.backgroundColor = active_color;

                images[carrent_img].classList.remove("show");
                images[j].classList.add("show");
                carrent_img = j;
            })  
        })(j);
    }
 }