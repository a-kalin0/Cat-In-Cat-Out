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

$('#modal-1').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset');
    // Reset image preview to default image
    $('#imgFrontPreview').attr('src', "{% static 'CICO/img/silhouette%20face.jpg' %}");
});