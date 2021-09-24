if (isMobile){
        document.getElementById('confirm').style.width ='100%';     
    }

$(function() {
      $('#code').on('click', function(e) {
        e.preventDefault()
        $.getJSON('/send_confirmation_code',
            function(data) {
                $('#msg-category').css('display','block');
                $('#msg-category').addClass(data.add).removeClass(data.rem);
                $('#msg-content').text(data.msg);
                }
        );
        return false;
      });
    });