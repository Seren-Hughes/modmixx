document.addEventListener('DOMContentLoaded', function() {
    

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
        changeAudioBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Reset to upload state
            document.getElementById('audioUploadArea').style.display = 'block';
            document.getElementById('audioPreview').style.display = 'none';
            // Clear the file input
            document.getElementById('audioFileInput').value = '';
        });
    }
    
    if (changeImageBtn) {
        changeImageBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Reset to upload state
            document.getElementById('imageUploadArea').style.display = 'block';
            document.getElementById('imagePreview').style.display = 'none';
            // Clear the file input
            document.getElementById('imageFileInput').value = '';
        });
    }

    // Get all file drop zones
    const dropZones = document.querySelectorAll('.upload-drop-zone');

    dropZones.forEach(dropZone => {
        const fileInput = dropZone.querySelector('input[type="file"]');
        
        if (!fileInput) return;
        
        // single change event listener for each file input
        fileInput.addEventListener('change', function(e) {
            e.stopPropagation();
            
            const file = e.target.files[0];
            if (file) {
                console.log('File selected:', file.name); // Debug
                
                // Determine if it's audio or image
                if (fileInput.id === 'audioFileInput') {
                    showAudioPreview(file);
                } else if (fileInput.id === 'imageFileInput') {
                    showImagePreview(file);
                }
            }
        });
        
        // Prevent default drag behaviours - this is important for drag and drop to work
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
        
        // Handle file drop
        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                console.log('File dropped:', files[0].name); // Debug
                
                // Assign the file directly
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(files[0]);
                fileInput.files = dataTransfer.files;
                
                // Trigger change event 
                fileInput.dispatchEvent(new Event('change'));
            }
        });
        
        // Click to open file picker
        dropZone.addEventListener('click', (e) => {
            e.stopPropagation();
            // Only trigger if clicking the zone, not the input itself
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });
    });
});