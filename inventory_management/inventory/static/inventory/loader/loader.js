jQuery(function($) {
	var spinner = $('#loader');
  	$("#mark_done_form").on("submit", function(){
    	spinner.fadeIn();
  	});
});