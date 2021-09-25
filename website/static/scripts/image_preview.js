const upload= document.getElementById('profile_img_upload');
const img = document.getElementById('profile_img');

upload.addEventListener('change', function(){
    const file = this.files[0];

    if (file){
        const reader = new FileReader();
        reader.addEventListener('load',function(){
            img.setAttribute('src',this.result);
        });
        reader.readAsDataURL(file);
    }
});