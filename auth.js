// Authentication protection for MOSAIC website
// This script should be included at the top of every protected page

(function() {
    // Check if user is authenticated
    function isAuthenticated() {
        const authStatus = sessionStorage.getItem('mosaicAuth');
        const authTime = parseInt(sessionStorage.getItem('mosaicAuthTime'));
        const currentTime = Date.now();
        const sessionDuration = 24 * 60 * 60 * 1000; // 24 hours
        
        if (authStatus === 'true' && authTime && (currentTime - authTime < sessionDuration)) {
            return true;
        }
        
        // Clear expired session
        sessionStorage.removeItem('mosaicAuth');
        sessionStorage.removeItem('mosaicAuthTime');
        return false;
    }
    
    // Redirect to login if not authenticated
    function requireAuth() {
        if (!isAuthenticated()) {
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            window.location.href = `login.html?return=${currentPage}`;
        }
    }
    
    // Logout function
    function logout() {
        sessionStorage.removeItem('mosaicAuth');
        sessionStorage.removeItem('mosaicAuthTime');
        window.location.href = 'login.html';
    }
    
    // Add logout functionality to pages
    function addLogoutButton() {
        // Only add if not already present
        if (document.querySelector('.logout-button')) return;
        
        const logoutBtn = document.createElement('a');
        logoutBtn.href = '#';
        logoutBtn.className = 'logout-button';
        logoutBtn.innerHTML = 'Logout';
        logoutBtn.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(237, 137, 54, 0.9);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            z-index: 1000;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        `;
        
        logoutBtn.addEventListener('mouseover', function() {
            this.style.background = 'rgba(221, 107, 32, 0.9)';
            this.style.transform = 'translateY(-2px)';
        });
        
        logoutBtn.addEventListener('mouseout', function() {
            this.style.background = 'rgba(237, 137, 54, 0.9)';
            this.style.transform = 'translateY(0)';
        });
        
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
        
        document.body.appendChild(logoutBtn);
    }
    
    // Run authentication check when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            requireAuth();
            addLogoutButton();
        });
    } else {
        requireAuth();
        addLogoutButton();
    }
    
    // Download function for electronic brochure
    function downloadBrochure() {
        const link = document.createElement('a');
        link.href = 'Final Mosaic One Pager.pdf';
        link.download = 'MOSAIC-Electronic-Brochure.pdf';
        link.target = '_blank';
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Optional: Track download event
        if (typeof gtag !== 'undefined') {
            gtag('event', 'download', {
                'event_category': 'engagement',
                'event_label': 'Electronic Brochure'
            });
        }
    }
    
    // Make functions available globally
    window.mosaicLogout = logout;
    window.downloadBrochure = downloadBrochure;
})();