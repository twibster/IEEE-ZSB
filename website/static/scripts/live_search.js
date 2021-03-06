$(document).ready(function(){
  var typingTimer;                //timer identifier
  var doneTypingInterval = 500;  //time in ms

  //on keyup, start the countdown
  $('#search').keyup(function(){
      clearTimeout(typingTimer);
      if ($('#search').val()) {
          typingTimer = setTimeout(doneTyping, doneTypingInterval);
      }
  });
  //run when user is "finished typing,"
  function doneTyping () {
      $('#result').html('')
      text = $('#search').val(); //store the data of the field
      $('#result').show();
      $.ajax({
        method:'post',
        url:'/livesearch',
        data:{text:text},
        success:function(result){
          console.log(result)
           $.each(result, function(key, value){ //loop through the query
              if (key.indexOf('__d__')!= -1){  //if the key of the record is a department
                $('#result').append('<a class="no-dec" href="/department/'+value.department+'"><li class="list-group-item link-class">'+value.department+' | <span class="text-muted">'+value.tasks+'</span></li></a>');
              }
              else if (key.indexOf('__t__')!= -1){
                $('#result').append('<a class="no-dec" href="/task/'+value.department+'/'+value.id+'-0"><li class="list-group-item link-class">'+value.title+' | <span class="text-muted">'+value.department+'</span><small class="author-name"> by '+value.last_name+'</small></li></a>');
              }
              else{ //if the key of the record is a user
                $('#result').append('<a class="no-dec" href="/profile/'+value.username+'"><li class="list-group-item link-class"><img src="/static/profile_pics/'+value.image_file+'"class="rounded-circle noti-img" />'+value.first_name+" "+value.last_name+' | <span class="text-muted">'+value.position+'</span></li></a>');
              }
           })
           $(document).click(function() { //hide the result if user clicks out of the content
                var container = $("#result");
                if (!container.is(event.target) && !container.has(event.target).length) {
                    container.hide();
                }
            });
        }
      })
    }
});