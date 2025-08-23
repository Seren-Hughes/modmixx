/* global bootstrap, DataTransfer */ // for jshint: globals objects provided by browser/bootstrap
/**
 * Track Upload Modal Management
 * 
 * Features:
 * - Drag & drop file upload with previews
 * - Form validation and error handling
 * - Modal state preservation on validation errors
 * - File type validation and preview generation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Modal state management for validation errors
    handleModalValidationErrors();
    
    
    function handleModalValidationErrors() {
        const uploadModal = document.getElementById('uploadModal');
        if (uploadModal && uploadModal.dataset.showModal === 'true') {
            const modal = new bootstrap.Modal(uploadModal);
            modal.show();
        }
    }
    
    // Handle modal reopening for validation errors
    const uploadModal = document.getElementById('uploadModal');
    
    if (uploadModal) {
        const showModal = uploadModal.dataset.showModal === 'true';
        
        if (showModal) {
            console.log('Reopening modal due to validation errors');
            const modal = new bootstrap.Modal(uploadModal);
            modal.show();
        }
        
        // Fix cancel button
        const cancelBtn = document.getElementById('cancelBtn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🐛 DEBUG: Cancel button clicked');
                
                // Force close the modal
                const modal = bootstrap.Modal.getInstance(uploadModal);
                if (modal) {
                    modal.hide();
                } else {
                    // If no instance exists, create one and hide it
                    const newModal = new bootstrap.Modal(uploadModal);
                    newModal.hide();
                }
                
                // Reset form
                const form = uploadModal.querySelector('form');
                if (form) {
                    form.reset();
                }
                
                // Reset preview areas
                resetPreviews();
                
                // Clear validation states
                clearAllValidationStates();
            });
        }
    }

    // Function to reset preview areas
    function resetPreviews() {
        // Reset audio preview
        const audioUploadArea = document.getElementById('audioUploadArea');
        const audioPreview = document.getElementById('audioPreview');
        if (audioUploadArea && audioPreview) {
            audioUploadArea.style.display = 'block';
            audioPreview.style.display = 'none';
        }
        
        // Reset image preview
        const imageUploadArea = document.getElementById('imageUploadArea');
        const imagePreview = document.getElementById('imagePreview');
        if (imageUploadArea && imagePreview) {
            imageUploadArea.style.display = 'block';
            imagePreview.style.display = 'none';
        }
    }

    // Function to clear all validation states
    function clearAllValidationStates() {
        const uploadModal = document.getElementById('uploadModal');
        if (uploadModal) {
            // Remove all error classes
            const invalidFields = uploadModal.querySelectorAll('.is-invalid');
            invalidFields.forEach(field => field.classList.remove('is-invalid'));
            
            // Hide all error messages
            const errorFeedbacks = uploadModal.querySelectorAll('.invalid-feedback');
            errorFeedbacks.forEach(feedback => feedback.style.display = 'none');
            
            // Remove error alerts
            const errorAlerts = uploadModal.querySelectorAll('.alert-danger');
            errorAlerts.forEach(alert => alert.remove());
        }
    }

    // Also handle the X (close) button
    const closeBtn = uploadModal.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            console.log('🐛 DEBUG: Close (X) button clicked');
            resetPreviews();
            clearAllValidationStates();
        });
    }

    // Handle modal hidden event (when modal is fully closed)
    if (uploadModal) {
        uploadModal.addEventListener('hidden.bs.modal', function() {
            console.log('🐛 DEBUG: Modal fully closed');
            
            // Reset everything when modal is completely hidden
            const form = uploadModal.querySelector('form');
            if (form) {
                form.reset();
            }
            
            resetPreviews();
            clearAllValidationStates();
            
            // If we're on a page with validation errors, redirect to clean feed
            if (uploadModal.dataset.showModal === 'true') {
                console.log('🐛 DEBUG: Redirecting to clean feed');
                window.location.href = '/';  // Redirect to clean feed
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

    // Clear form errors when user starts making changes
    function clearFieldErrors(fieldName) {
        const field = document.querySelector(`[name="${fieldName}"]`);
        if (field) {
            field.classList.remove('is-invalid');
            const feedback = field.parentNode.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.style.display = 'none';
            }
        }
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
            // Clear any validation errors
            clearFieldErrors('audio_file');
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
            // Clear any validation errors
            clearFieldErrors('track_image');
        });
    }

    // Get all file drop zones
    const dropZones = document.querySelectorAll('.upload-drop-zone');

    dropZones.forEach(dropZone => {
        const fileInput = dropZone.querySelector('input[type="file"]');
        
        if (!fileInput) return;
        
        // Single change event listener for each file input
        fileInput.addEventListener('change', function(e) {
            e.stopPropagation();
            
            const file = e.target.files[0];
            if (file) {
                console.log('File selected:', file.name, 'Type:', file.type); // Enhanced debug
                
                // Clear any existing validation errors
                clearFieldErrors(fileInput.name);
                
                // Determine if it's audio or image
                if (fileInput.id === 'audioFileInput') {
                    showAudioPreview(file);
                } else if (fileInput.id === 'imageFileInput') {
                    showImagePreview(file);
                }
            }
        });
        
        // Prevent default drag behaviours
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
                console.log('File dropped:', files[0].name, 'Type:', files[0].type); // Enhanced debug
                
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

    // Clear validation errors when user types in text fields
    const titleInput = document.querySelector('[name="title"]');
    const descriptionInput = document.querySelector('[name="description"]');
    
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            clearFieldErrors('title');
        });
    }
    
    if (descriptionInput) {
        descriptionInput.addEventListener('input', function() {
            clearFieldErrors('description');
        });
    }

    // Reset modal state when it's closed
    if (uploadModal) {
        uploadModal.addEventListener('hidden.bs.modal', function() {
            // Reset all form fields and previews
            const form = uploadModal.querySelector('form');
            if (form) {
                form.reset();
            }
            
            // Reset previews
            document.getElementById('audioUploadArea').style.display = 'block';
            document.getElementById('audioPreview').style.display = 'none';
            document.getElementById('imageUploadArea').style.display = 'block';
            document.getElementById('imagePreview').style.display = 'none';
            
            // Clear all validation states
            const invalidFields = uploadModal.querySelectorAll('.is-invalid');
            invalidFields.forEach(field => field.classList.remove('is-invalid'));
            
            const errorAlerts = uploadModal.querySelectorAll('.alert-danger');
            errorAlerts.forEach(alert => alert.remove());
        });
    }
});