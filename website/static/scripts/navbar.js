$(function() {
  $(document).click(function (event) {
    var navbar=$(".navbar-collapse")

    //set result width equal to the search fiedl width
    if ((navbar.is(":visible")) && (result.offsetWidth != search.offsetWidth) && (isMobile))
      search_div.style.width ='100%'
      result.style.width = search.offsetWidth;
      
    //hide the navbar when user cliks outside of the content of the navbar
    if (!navbar.is(event.target) && !navbar.has(event.target).length && (isMobile))
      navbar.collapse('hide'); 
  });
});
