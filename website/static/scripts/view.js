sidebar = document.getElementById('sidebar');
logo = document.getElementById('logo');
nav_elements_mobile = document.getElementById('nav-elements-mobile');
reg_desktop = document.getElementById('desktop');
reg_mobile = document.getElementById('mobile');
user_info_div = document.getElementById('reg-user-info-div');
notifications_icon_desktop = document.getElementById('notifications-icon-desktop');
notifications_icon_mobile = document.getElementById('notifications-icon-mobile');

var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (isMobile) {
  if (sidebar){
    sidebar.parentNode.removeChild(sidebar);
  }
  else if (reg_desktop){
    reg_desktop.parentNode.removeChild(reg_desktop); 
  }
  notifications_icon_desktop.parentNode.removeChild(notifications_icon_desktop); 
}
else{
  if (reg_mobile){
    reg_mobile.parentNode.removeChild(reg_mobile);
    user_info_div.classList.add("reg-user-info");
  }
  logo.classList.add("navbar-brand-desktop");
  notifications_icon_mobile.parentNode.removeChild(notifications_icon_mobile);
  nav_elements_mobile.parentNode.removeChild(nav_elements_mobile);
  }