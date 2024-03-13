$(document).ready(function(){
	$(".invisible").hide();
	$(document).on('click', "#btn", function(){
		var lessmorebtn = $(".invisible").is(":visible")?'Read More':'Read Less';
		$(this).text(lessmorebtn);
		$(this).parent(".box").find(".invisible").toggle();
		$(this).parent(".box").find(".content").toggle();
	});

});