document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const submitButton = document.getElementById('submitButton');

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (fileInput.files.length > 0) {
            uploadForm.submit();
        } else {
            alert('Please select a photo to upload.');
        }
    });
});