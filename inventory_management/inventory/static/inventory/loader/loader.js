jQuery(function($) {
	var spinner = $('#form_loader');
  	$("form").on("submit", function(){
    	spinner.show();
  	});//submit
});//document ready