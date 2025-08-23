function connectGoogle() {
      const url = "/3rdparty/";
      const popup = window.open(
        url, 
        'google_connect', 
        'width=500,height=600,scrollbars=yes,resizable=yes,toolbar=no,menubar=no,location=no,status=no'
      );
      
      // Monitor when popup closes and check if user is still logged in
      const checkClosed = setInterval(() => {
        if (popup.closed) {
          clearInterval(checkClosed);
          
          // Check if user is still logged in by making a simple request
          fetch('/profile/edit/', {
            method: 'HEAD',
            credentials: 'same-origin'
          })
          .then(response => {
            if (response.status === 302 || response.status === 401) {
              // User was logged out in popup, redirect to home
              window.location.href = '/';
            } else {
              // User is still logged in, refresh to show any changes
              window.location.reload();
            }
          })
          .catch(() => {
            // On error, assume logout and redirect to home
            window.location.href = '/';
          });
        }
      }, 1000);
    }