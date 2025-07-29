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
                    // temporary solution to show comment changes: reload the page
                    window.location.reload();
                } else {
                    alert('Error saving comment');
                }
            });
        });
    });

    // Delete comment
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this comment?')) {
                const commentId = this.dataset.commentId;
                
                fetch(`/comments/delete/${commentId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // temporary solution to show comment deletion: reload the page
                        window.location.reload();
                    } else {
                        alert('Error deleting comment');
                    }
                });
            }
        });
    });
});