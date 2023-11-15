function updateImagePreview(input, imageId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById(imageId).src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]);   
    }
}

window.updateImagePreview = updateImagePreview;