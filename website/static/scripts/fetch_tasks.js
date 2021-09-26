$(document).ready(function(){
	var typingTimer;                //timer identifier
  	var doneTypingInterval = 500;  //time in ms
	var end= false

	var getData =function(){
		if (!(end)){
			$.getJSON('/get_tasks',
	            function(data) {
	            	console.log(data)
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
		    clearTimeout(typingTimer);
		    typingTimer = setTimeout(getData, doneTypingInterval);
	    }
	};
	getData()
});