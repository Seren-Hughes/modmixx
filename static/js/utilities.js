// Smooth scroll for anchor links (down arrow icon)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Toast notifications
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any toasts that exist
    document.querySelectorAll('.toast').forEach(function(toastNode) {
        new bootstrap.Toast(toastNode, { delay: 4000, autohide: true }).show();
    });
});