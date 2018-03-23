// will change ..static/ to python url_for function
window.onload = function(){
	var owl = $('.owl-carousel');
					owl.owlCarousel({
						items:1,
						responsiveClass:true,
						nav: true,			
						navText: [
							'<img style="display:block" class="am-prew" src="../static/img/left.svg" alt="">',
							'<img style="display:block" class="am-prew" src="../static/img/right.svg" alt="">'
						],
						singleItem:true,
						loop:true,
						// margin:10,
						autoplayHoverPause:true,
						autoWidth:true,
						autoplay:true,
						autoplayTimeout:3000,
						autoplaySpeed:1000
					});
}
