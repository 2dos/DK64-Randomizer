// Handle mobile navbar toggle to push sidebar down
function setupMobileNavbarToggle() {
    console.log('Window width:', window.innerWidth);

    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('#navbarResponsive');
    const sidebar = document.querySelector('#nav-tab-list');

    console.log('Found elements:', {
        navbarToggler: !!navbarToggler,
        navbarCollapse: !!navbarCollapse,
        sidebar: !!sidebar
    });

    if (!navbarToggler || !navbarCollapse || !sidebar) {
        console.error('Missing required elements');
        return;
    }

    // Listen to Bootstrap collapse events - 'show'/'hide' fire at START of animation
    navbarCollapse.addEventListener('show.bs.collapse', function() {
        sidebar.style.top = '212px';
    });

    navbarCollapse.addEventListener('hide.bs.collapse', function() {
        sidebar.style.top = '70px';
    });
}

// Wait for sidebar to be rendered and setup
const checkSidebar = setInterval(function() {
    const sidebar = document.querySelector('#nav-tab-list');
    if (sidebar) {
        clearInterval(checkSidebar);
        setupMobileNavbarToggle();
    }
}, 100);

setTimeout(function() {
    clearInterval(checkSidebar);
}, 5000);
