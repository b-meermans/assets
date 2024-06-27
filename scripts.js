document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname.toLowerCase();

    // Highlight the active menu and submenu items
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const menuLink = dropdown.querySelector('a').getAttribute('href').toLowerCase();
        const submenuLinks = dropdown.querySelectorAll('.dropdown-content a');

        // Check if the main menu item should be active
        if (path.includes(menuLink)) {
            dropdown.querySelector('a').classList.add('active-menu');
        }

        // Check if any submenu item should be active
        submenuLinks.forEach(submenuLink => {
            if (path.includes(submenuLink.getAttribute('href').toLowerCase())) {
                submenuLink.classList.add('active-submenu');
                // Ensure the main menu item is also highlighted
                dropdown.querySelector('a').classList.add('active-menu');
            }
        });
    });
});

function toggleMenu() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('active');
}

// Event listeners for dropdown menus
document.querySelectorAll('.dropdown > a').forEach(item => {
    item.addEventListener('click', function(event) {
        event.preventDefault();
        // Hide other open dropdowns
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            if (dropdown !== this.parentElement) {
                dropdown.classList.remove('active');
            }
        });
        // Toggle the clicked dropdown
        this.parentElement.classList.toggle('active');
    });
});

document.addEventListener('click', function(event) {
    if (!event.target.closest('.menu')) {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});
