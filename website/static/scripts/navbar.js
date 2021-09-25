$(function() {
  $(document).click(function (event) {
    container=$(".navbar-collapse")
    if (!container.is(event.target) && !container.has(event.target).length)
      container.collapse('hide');
  });
});