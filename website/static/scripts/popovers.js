//initialize popovers
$(function () {
$('[data-toggle="popover"]').popover()})

//make popovers disappear on next click outside the popover
$("html").on("mouseup", function (e) {
  var l = $(e.target);
  if (l[0].className.indexOf("popover") == -1) {
      $(".popover").each(function () {
          $(this).popover("hide");
      });
  }
});