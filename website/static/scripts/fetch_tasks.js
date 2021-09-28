$(document).ready(function(){
	var waiting_timer;                //timer identifier
  	var wait_befor_request = 300;  //time in ms
	var end= false

	var getData =function(){
		if (!(end)){
			$.getJSON('/get_tasks',
	            function(data) {
	            	end = jQuery.isEmptyObject(data.tasks)
	            	if (!(end)){
		                $('#preview').append(data.tasks)
		            }
		            else{
		            	$('#preview').append('<p style="text-align:center;">End of results</p>')
		            }
	            }
	        );
		}
	};
	window.onscroll = function(ev) {
	    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
		    clearTimeout(waiting_timer);
		    waiting_timer = setTimeout(getData, wait_befor_request);
	    }
	};
	getData()
});