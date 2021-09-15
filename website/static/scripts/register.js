if (isMobile){
    reg_desktop = document.getElementById('desktop');
    reg_desktop.parentNode.removeChild(reg_desktop);
}
else{
    user_info_div = document.getElementById('reg-user-info-div');
    reg_mobile = document.getElementById('mobile');
    reg_mobile.parentNode.removeChild(reg_mobile);
    user_info_div.classList.add("reg-user-info");
} 
 
document.addEventListener("DOMContentLoaded", function() {

    position = document.getElementById('position');
    diff_pos =document.getElementById('diff_pos');
    department_div =document.getElementById('department_div');
    checked = document.getElementById('team_leader');

    function pos(){
        state = position.value;
        if (state == 'IEEE Chairman'  || state== 'Vice Technical' || state== 'RAS Chairman' || state=='RAS Vice Chairman') {
            department.selectedIndex= 0;
            department_div.style.display='none';
            diff_pos.style.display='block';  
        }   
        else if ( state== 'Team Leader' || state=='Team Member'){
            department_div.style.display='block';
            diff_pos.style.display='none';
            checked.checked =false;
        }
        else{
            department_div.style.display='none';
            department=document.getElementById('department');
            department.selectedIndex= 1;
            diff_pos.style.display='none';
            checked.checked =false
            }}
    function leader(){
        if (checked.checked ==true){
            department_div.style.display='block';
        }
        else{
            department_div.style.display='none';
        }
    }
    pos()
    leader()
    position.onchange =function(){
        pos();
    }
    checked.onchange =function(){
        leader();
}});