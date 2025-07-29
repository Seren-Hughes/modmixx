// fetch API - 
// https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Network_requests
// https://javascript.info/fetch
// https://stackoverflow.com/questions/75034532/django-ajax-comments

document.addEventListener('DOMContentLoaded', function() {
    // Edit comment functionality
    document.querySelectorAll('.edit-comment').forEach(button => {
        button.addEventListener('click', function() {
            const comment = this.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            
            content.style.display = 'none';
            editForm.style.display = 'block';
            editForm.querySelector('textarea').focus();
        });
    });

    // Cancel edit
    document.querySelectorAll('.cancel-edit').forEach(button => {
        button.addEventListener('click', function() {
            const comment = this.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            
            content.style.display = 'block';
            editForm.style.display = 'none';
        });
    });

    // Save comment 
    document.querySelectorAll('.save-comment').forEach(button => {
        button.addEventListener('click', function() {
            const comment = this.closest('[data-comment-id]');
            const commentId = comment.dataset.commentId;
            const textarea = comment.querySelector('textarea');
            const newContent = textarea.value;

            fetch(`/comments/edit/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `content=${encodeURIComponent(newContent)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update content in place (no reload!)
                    const content = comment.querySelector('.comment-content');
                    const editForm = comment.querySelector('.comment-edit-form');
                    
                    // Update the displayed content
                    content.innerHTML = data.content.replace(/\n/g, '<br>');
                    content.style.display = 'block';
                    editForm.style.display = 'none';
                    
                    // Add or update "edited" indicator
                    let editedSpan = comment.querySelector('.edited-indicator');
                    if (!editedSpan) {
                        editedSpan = document.createElement('span');
                        editedSpan.className = 'text-muted small ms-1 edited-indicator';
                        editedSpan.textContent = '(edited)';
                        comment.querySelector('.text-muted.small').insertAdjacentElement('afterend', editedSpan);
                    }
                } else {
                    alert('Error saving comment');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving comment');
            });
        });
    });

    // Delete comment 
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this comment?')) {
                const commentId = this.dataset.commentId;
                
                // comment container (li element) not the button!
                const comment = document.querySelector(`li[data-comment-id="${commentId}"]`);
                
                fetch(`/comments/delete/${commentId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Remove the comment element from the DOM
                        if (comment) {
                            comment.remove(); // Simple removal
                        } else {
                            alert('Error deleting comment: Comment element not found');
                        }
                    }
                })
            }
        });
    });
});