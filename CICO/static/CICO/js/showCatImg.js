function updateImagePreview(inputId, imageId) {
    document.getElementById(inputId).addEventListener('change', function (event) {
        const input = event.target;
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                document.getElementById(imageId).src = e.target.result;
            }

            reader.readAsDataURL(input.files[0]);   
        }
    });
}

updateImagePreview('imgFrontInput', 'imgFrontPreview');
updateImagePreview('imgBackInput', 'imgBackPreview');
updateImagePreview('imgLeftInput', 'imgLeftPreview');
updateImagePreview('imgRightInput', 'imgRightPreview');