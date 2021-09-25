$(document).ready(function(){
  var typingTimer;                //timer identifier
  var doneTypingInterval = 200;  //time in ms

  //on keyup, start the countdown
  $('#search').keyup(function(){
      clearTimeout(typingTimer);
      if ($('#search').val()) {
          typingTimer = setTimeout(doneTyping, doneTypingInterval);
      }
  });
  //runs when user is "finished typing,"
  function doneTyping () {
      $('#result').html('')
      text = $('#search').val(); //store the data of the field
      $.ajax({
        method:'post',
        url:'/livesearch',
        data:{text:text},
        success:function(result){
           $.each(result, function(key, value){ //loop through the query
              if (key.indexOf('__d__')!= -1){  //if the key of the record is a department
                $('#result').append('<a class="no-dec" href="/'+value.department+'"><li class="list-group-item link-class">'+value.department+' | <span class="text-muted">'+value.tasks+'</span></li></a>');
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