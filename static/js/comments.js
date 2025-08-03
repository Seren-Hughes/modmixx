/*
    References:
    - fetch API: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Network_requests
    - fetch tutorial: https://javascript.info/fetch
    - Django AJAX comments: https://stackoverflow.com/questions/75034532/django-ajax-comments
*/

// AJAX comment functionality for modmixx
// Uses fetch API for edit/delete actions and updates DOM instantly
// Toast notifications for user feedback

document.addEventListener('DOMContentLoaded', function() {
    // Edit comment: show edit form, hide content
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

    // Cancel edit: hide edit form, show content
    document.querySelectorAll('.cancel-edit').forEach(button => {
        button.addEventListener('click', function() {
            const comment = this.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            content.style.display = 'block';
            editForm.style.display = 'none';
        });
    });

    // Save comment: send AJAX, update DOM in place
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
                    // Update comment content and hide edit form
                    const content = comment.querySelector('.comment-content');
                    const editForm = comment.querySelector('.comment-edit-form');
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
                    showToast('Comment updated!');
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

    // Delete comment: send AJAX, remove from DOM, update badge, show toast
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this comment?')) {
                const commentId = this.dataset.commentId;
                const comment = document.querySelector(`.card[data-comment-id="${commentId}"]`);

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
                        if (comment) {
                            comment.remove();

                            // Update comment count badge
                            const badge = document.querySelector('.badge.bg-secondary.ms-2');
                            if (badge) {
                                let count = parseInt(badge.textContent, 10);
                                badge.textContent = Math.max(count - 1, 0);
                            }

                            // Show toast notification
                            showToast('Comment deleted successfully!');
                        } else {
                            alert('Error deleting comment: Comment element not found');
                        }
                    }
                });
            }
        });
    });
});

// Simple toast notification (Bootstrap)
function showToast(message) {
    let toast = document.createElement('div');
    toast.className = 'toast align-items-center text-bg-success border-0 show position-fixed bottom-0 end-0 m-3';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}