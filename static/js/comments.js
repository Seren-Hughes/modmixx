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
// Toast notifications for user feedback

document.addEventListener('DOMContentLoaded', function() {

    // Use event delegation for all comment actions (works for new comments too)
    document.addEventListener('click', function(e) {
        // Edit button: show edit form, hide comment content
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

        // Cancel edit: hide edit form, show comment content again
        if (e.target.classList.contains('cancel-edit')) {
            const comment = e.target.closest('[data-comment-id]');
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            if (content && editForm) {
                content.style.display = 'block';
                editForm.style.display = 'none';
            }
        }

        // Save edited comment: send AJAX, update DOM in place
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
                        const timeElement = comment.querySelector('.text-muted.small');
                        if (timeElement) {
                            timeElement.insertAdjacentElement('afterend', editedSpan);
                        }
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
        }

        // Delete comment
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
                                // Show "[deleted comment]" and hide actions
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
                                // Remove comment from DOM
                                comment.remove();
                                updateCommentCount(-1);
                                // Clean up any empty soft-deleted parents
                                if (data.parent_cleanup && data.parent_cleanup.length > 0) {
                                    data.parent_cleanup.forEach(parentId => {
                                        const parentComment = document.querySelector(`[data-comment-id="${parentId}"]`);
                                        if (parentComment) {
                                            parentComment.remove();
                                        }
                                    });
                                    showToast(
                                        data.parent_cleanup.length === 1
                                            ? 'Empty parent comment cleaned up'
                                            : `${data.parent_cleanup.length} empty parent comments cleaned up`
                                    );
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

        // Toggle reply form
        if (e.target.classList.contains('reply-btn')) {
            const card = e.target.closest('.card-body');
            const form = card.querySelector('.reply-form');
            if (form) {
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }
        }
    });

    // Handle form submissions (main comment and replies)
    document.addEventListener('submit', function(e) {
        // Reply form
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
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Add the new reply under the parent comment
                    const parentCard = document.querySelector(`[data-comment-id="${parentId}"]`);
                    parentCard.insertAdjacentHTML('beforeend', data.comment_html);
                    form.reset();
                    form.style.display = 'none';
                    updateCommentCount(1);
                    showToast('Reply posted successfully!');
                } else {
                    console.error('Error:', data.errors);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        // Main comment form
        if (e.target.id === 'comment-form' || e.target.classList.contains('main-comment-form')) {
            e.preventDefault();
            const form = e.target;
            const trackId = form.querySelector('input[name="track"]').value;
            const content = form.querySelector('textarea[name="content"]').value;

            if (!content.trim()) {
                alert('Please enter a comment');
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
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentsList = document.querySelector('.comments-list');
                    commentsList.insertAdjacentHTML('afterbegin', data.comment_html);
                    form.reset();
                    updateCommentCount(1);
                    showToast('Comment posted successfully!');
                } else {
                    console.error('Error:', data.errors);
                    alert('Error posting comment');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error posting comment');
            });
        }
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

// getCookie adapted from Django docs: https://docs.djangoproject.com/en/5.2/howto/csrf/#:~:text=getCookie%28name%29%20%7B
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

// Update the comment count badge
function updateCommentCount(delta) {
    const countElem = document.getElementById('comment-count');
    if (countElem) {
        let count = parseInt(countElem.textContent, 10) || 0;
        countElem.textContent = count + delta;
    }
}