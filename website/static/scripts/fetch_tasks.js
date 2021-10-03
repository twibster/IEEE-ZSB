$(document).ready(function(){
	first =true
	try {
	    document.getElementById('filter').onclick = function() {
		department= department=document.getElementById('department').value
		sort = sort=document.getElementById('sort').value
		method = method=document.getElementById('method').value
		first= end =false
		transition = true
   		getData(department,sort,method,transition)
   		};
	  } catch (e) {
	      if (e instanceof TypeError) {
	          console.log(e)
	      }
	  }

	var waiting_timer;                //timer identifier
  	var wait_befor_request = 300;  	  //time in ms
	var end= false
	var getData =function(department,sort,method,transition){
		if (!(end)){
			if (typeof department !== 'undefined'){
				if (transition){
				 	url='/get_tasks?department='+department+'&sort='+sort+'&method='+method+'&butt=true'
				}
				else{
					url='/get_tasks?department='+department+'&sort='+sort+'&method='+method+''
				}
			}
			else{
				url='/get_tasks'
			}
			$.getJSON(url,
	            function(data) {
	            	end = jQuery.isEmptyObject(data.tasks)
	            	if (!(end)){
	            		if (transition){
	            			$('#preview').empty().append(data.tasks)
	            			transition=false
	            		}
	            		else{
	            			$('#preview').append(data.tasks)
	            		}       
		            }
		            else{
		            	if (transition){
		            		$('#preview').empty().append('<p style="text-align:center;">WoW, such empty!</p>')
		            	}
		            	else{
		            		$('#preview').append('<p style="text-align:center;">End of results</p>')
		            	}
		            }
	            }
	        );
		}
	};
	getData()
	window.onscroll = function(ev) {
	    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
		    clearTimeout(waiting_timer);
		    if (first ==true){
		    	waiting_timer = setTimeout(getData, wait_befor_request);
		    }
		    else{
		    	waiting_timer = setTimeout(getData, wait_befor_request,department,sort,method);
		    }   
	    }
	};
});