let state=document.getElementById('state');
state.onchange = function () {
    type =state.value;
    map_object=document.getElementById('map_object');
    if (type =='Online'){
        map_object.style.display='none'
    }
    else
        map_object.style.display='block'
}