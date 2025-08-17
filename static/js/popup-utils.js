document.addEventListener('DOMContentLoaded', function() {
    // Check if this is a popup/connect flow
    if (window.location.search.includes('process=connect') || 
        document.querySelector('.social-connections-container')) {
        
        const navbar = document.querySelector('nav.navbar');
        const footer = document.querySelector('footer');
        
        if (navbar) navbar.style.display = 'none';
        if (footer) footer.style.display = 'none';
        
        // Center content for popup
        document.body.style.display = 'flex';
        document.body.style.alignItems = 'center';
        document.body.style.justifyContent = 'center';
        document.body.style.minHeight = '100vh';
        document.body.style.margin = '0';
    }
});