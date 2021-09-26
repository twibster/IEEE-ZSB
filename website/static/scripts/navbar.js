$(function() {
  $(document).click(function (event) {
    container=$(".navbar-collapse")

    //set result width equal to the search fiedl width
    if ((container.is(":visible")) && (result.offsetWidth != search.offsetWidth)) 
      search_div.style.width ='100%'
      result.style.width = search.offsetWidth;
      
    //hide the navbar when user cliks outside of the content of the navbar
    if (!container.is(event.target) && !container.has(event.target).length)
      container.collapse('hide'); 
  });
});
