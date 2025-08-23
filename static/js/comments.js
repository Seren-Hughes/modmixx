/*
    References:
    - fetch API: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Network_requests
    - fetch tutorial: https://javascript.info/fetch
    - Django AJAX comments: https://stackoverflow.com/questions/75034532/django-ajax-comments
    - Event delegation: https://www.freecodecamp.org/news/event-delegation-javascript/
    - Event delegation (dev.to): https://dev.to/js_bits_bill/event-delegation-with-vanilla-js-js-bits-2lnb
*/

// AJAX comment functionality for modmixx
// Uses event delegation and fetch API for edit/delete actions and updates DOM instantly
// Toast notifications for user feedback and toxicity moderation with clear error messages

document.addEventListener('DOMContentLoaded', function() {

    // Use event delegation for all comment actions - works for dynamically added comments too
    document.addEventListener('click', function(e) {
        
        // Edit button: swap comment content for edit form, focus textarea
        if (e.target.classList.contains('edit-comment')) {
            const comment = e.target.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            if (content && editForm) {
                content.style.display = 'none';
                editForm.style.display = 'block';
                editForm.querySelector('textarea').focus();
            }
        }

        // Cancel edit: revert back to original comment display
        if (e.target.classList.contains('cancel-edit')) {
            const comment = e.target.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            if (content && editForm) {
                content.style.display = 'block';
                editForm.style.display = 'none';
            }
        }

        // Save edited comment: AJAX update, refresh DOM content in place
        if (e.target.classList.contains('save-comment')) {
            const comment = e.target.closest('[data-comment-id]');
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
                    // Update comment content with new text and hide edit form
                    const content = comment.querySelector('.comment-content');
                    const editForm = comment.querySelector('.comment-edit-form');
                    content.innerHTML = data.content.replace(/\n/g, '<br>');
                    content.style.display = 'block';
                    editForm.style.display = 'none';

                    // Add "(edited)" indicator if it doesn't exist yet
                    let editedSpan = comment.querySelector('.edited-indicator');
                    if (!editedSpan) {
                        editedSpan = document.createElement('span');
                        editedSpan.className = 'text-muted small ms-1 edited-indicator';
                        editedSpan.textContent = '(edited)';
                        const timeElement = comment.querySelector('.text-muted.small');
                        if (timeElement) {
                            timeElement.insertAdjacentElement('afterend', editedSpan);
                        }
                    }
                    showToast('Comment updated!');
                } else {
                    // Handle toxicity/validation errors for edits
                    if (data.errors && data.errors.content && data.errors.content[0]) {
                        const editForm = comment.querySelector('.comment-edit-form');
                        showCommentError(data.errors.content[0], editForm);
                    } else {
                        alert('Error saving comment');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving comment');
            });
        }

        // Delete comment: soft or hard delete with parent cleanup logic
        if (e.target.classList.contains('delete-comment')) {
            if (confirm('Are you sure you want to delete this comment?')) {
                const commentId = e.target.dataset.commentId;
                const comment = document.querySelector(`[data-comment-id="${commentId}"]`);

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
                            if (data.delete_type === 'soft') {
                                // Soft delete: show "[deleted comment]" placeholder, hide actions
                                const commentContent = comment.querySelector('.comment-content');
                                const dropdown = comment.querySelector('.dropdown');
                                const replyButton = comment.querySelector('.reply-btn');
                                if (dropdown) dropdown.style.display = 'none';
                                if (replyButton) replyButton.style.display = 'none';
                                if (commentContent) {
                                    commentContent.innerHTML = '<em class="text-muted">[deleted comment]</em>';
                                }
                                updateCommentCount(-1);
                                showToast('Comment deleted (replies preserved)');
                            } else {
                                // Hard delete: remove from DOM completely
                                comment.remove();
                                updateCommentCount(-1);
                                
                                // Clean up any empty soft-deleted parent comments recursively
                                if (data.parent_cleanup && data.parent_cleanup.length > 0) {
                                    data.parent_cleanup.forEach(parentId => {
                                        const parentComment = document.querySelector(`[data-comment-id="${parentId}"]`);
                                        if (parentComment) {
                                            parentComment.remove();
                                        }
                                    });
                                    showToast(data.parent_cleanup.length === 1 ? 'Empty parent comment cleaned up' : `${data.parent_cleanup.length} empty parent comments cleaned up`);
                                }
                                showToast('Comment deleted successfully!');
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error deleting comment');
                });
            }
        }

        // Toggle reply form: show/hide inline reply textarea
        if (e.target.classList.contains('reply-btn')) {
            const card = e.target.closest('.card-body');
            const form = card.querySelector('.reply-form');
            if (form) {
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }
        }
    });

    // Handle form submissions - main comments and threaded replies
    document.addEventListener('submit', function(e) {
        
        // Reply form submission: nested under parent comment
        if (e.target.classList.contains('reply-form')) {
            e.preventDefault();
            const form = e.target;
            const parentId = form.querySelector('input[name="parent"]').value;
            const trackId = form.querySelector('input[name="track"]').value;
            const content = form.querySelector('textarea[name="content"]').value;

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams({
                    content: content,
                    parent: parentId,
                    track: trackId
                })
            })
            .then(response => {
                // Handle both success and 400 validation errors as JSON
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Add the new reply HTML under the parent comment
                    const parentCard = document.querySelector(`[data-comment-id="${parentId}"]`);
                    parentCard.insertAdjacentHTML('beforeend', data.comment_html);
                    form.reset();
                    form.style.display = 'none';
                    updateCommentCount(1);
                    showToast('Reply posted successfully!');
                } else {
                    // Show toxicity moderation or other validation errors to user
                    if (data.errors && data.errors.content && data.errors.content[0]) {
                        showCommentError(data.errors.content[0], form);
                    } else {
                        showCommentError('Error posting reply. Please try again.', form);
                    }
                }
            })
            .catch(error => {
                console.error('Network error:', error);
                showCommentError('Network error. Please try again.', form);
            });
        }

        // Main comment form submission: top-level comments
        if (e.target.id === 'comment-form' || e.target.classList.contains('main-comment-form')) {
            e.preventDefault();
            const form = e.target;
            const trackId = form.querySelector('input[name="track"]').value;
            const content = form.querySelector('textarea[name="content"]').value;

            // Basic client-side validation before sending to server
            if (!content.trim()) {
                showCommentError('Please enter a comment', form);
                return;
            }

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams({
                    content: content,
                    track: trackId
                })
            })
            .then(response => {
                // Handle both success and 400 validation errors as JSON
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Add new comment at the top of the comments list
                    const commentsList = document.querySelector('.comments-list');
                    commentsList.insertAdjacentHTML('afterbegin', data.comment_html);
                    form.reset();
                    updateCommentCount(1);
                    showToast('Comment posted successfully!');
                } else {
                    // Show toxicity moderation or other validation errors to user
                    if (data.errors && data.errors.content && data.errors.content[0]) {
                        showCommentError(data.errors.content[0], form);
                    } else {
                        showCommentError('Error posting comment. Please try again.', form);
                    }
                }
            })
            .catch(error => {
                console.error('Network error:', error);
                showCommentError('Network error. Please try again.', form);
            });
        }
    });
});

// Toast notifications using Bootstrap classes - success messages in bottom right
function showToast(message) {
    const toast = document.createElement('div');
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

// getCookie CSRF token helper adapted from Django docs: https://docs.djangoproject.com/en/5.2/howto/csrf/#:~:text=getCookie%28name%29%20%7B
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function(cookie) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                cookieValue = decodeURIComponent(value);
            }
        });
    }
    return cookieValue;
}

// Update the comment count badge in the track header
function updateCommentCount(delta) {
    const countElem = document.getElementById('comment-count');
    if (countElem) {
        const count = parseInt(countElem.textContent, 10) || 0;
        countElem.textContent = count + delta;
    }
}

// Show validation errors (toxicity, empty content) directly below comment forms
function showCommentError(message, form) {
    // Remove any existing error messages to avoid stacking
    const existingError = form.querySelector('.comment-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Create red alert with error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger mt-2 comment-error';
    errorDiv.textContent = message;
    
    // Insert error message after the textarea
    const textarea = form.querySelector('textarea[name="content"]');
    if (textarea) {
        textarea.parentNode.insertBefore(errorDiv, textarea.nextSibling);
        
        // Auto-remove error after 7 seconds so it doesn't clutter the UI
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 7000);
    }
}