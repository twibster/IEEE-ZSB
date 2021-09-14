//make navbar disappear on next click outside the collapsed content
$(function() {
  $(document).click(function (event) {
    $('.navbar-collapse').collapse('hide');
  });
});