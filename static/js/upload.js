document.addEventListener('DOMContentLoaded', function() {
    // Audio file preview
    const audioFileInput = document.getElementById('audioFileInput');
    
    if (audioFileInput) {
        audioFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                showAudioPreview(file);
            }
        });
    }

    // Image file preview
    const imageFileInput = document.getElementById('imageFileInput');
    
    if (imageFileInput) {
        imageFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                showImagePreview(file);
            }
        });
    }

    // Functions to show previews with change/remove buttons
    function showAudioPreview(file) {
        document.getElementById('audioUploadArea').style.display = 'none';
        document.getElementById('audioPreview').style.display = 'block';
        document.getElementById('audioFileName').textContent = file.name;
    }
    
    function showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imageUploadArea').style.display = 'none';
            document.getElementById('imagePreview').style.display = 'block';
            document.getElementById('previewImg').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // Change file buttons
    const changeAudioBtn = document.getElementById('changeAudioBtn');
    const changeImageBtn = document.getElementById('changeImageBtn');
    
    if (changeAudioBtn) {
        changeAudioBtn.addEventListener('click', function() {
            // Reset to upload state
            document.getElementById('audioUploadArea').style.display = 'block';
            document.getElementById('audioPreview').style.display = 'none';
            // Clear the file input
            document.getElementById('audioFileInput').value = '';
        });
    }
    
    if (changeImageBtn) {
        changeImageBtn.addEventListener('click', function() {
            // Reset to upload state
            document.getElementById('imageUploadArea').style.display = 'block';
            document.getElementById('imagePreview').style.display = 'none';
            // Clear the file input
            document.getElementById('imageFileInput').value = '';
        });
    }
});