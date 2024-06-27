function toggleMenu() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('active');
}

document.addEventListener('click', function(event) {
    if (!event.target.closest('.menu')) {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    const path = window.location.pathname.toLowerCase().replace('\\', '/');
    console.log('Current path:', path); // Debugging: Log the current path

    // Highlight the active menu and submenu items
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const menuLink = dropdown.querySelector('a').getAttribute('href').toLowerCase();
        const submenuLinks = dropdown.querySelectorAll('.dropdown-content a');

        console.log('Checking menu link:', menuLink); // Debugging: Log the menu link

        // Check if the main menu item should be active
        if (path === menuLink || path === menuLink + '/') {
            dropdown.querySelector('a').classList.add('active-menu');
            console.log('Main menu active:', menuLink); // Debugging: Log active main menu
        }

        // Check if any submenu item should be active
        submenuLinks.forEach(submenuLink => {
            const submenuHref = submenuLink.getAttribute('href').toLowerCase().replace('\\', '/');
            console.log('Sub:', submenuHref); // Debugging: Log the submenu link

            if (path === submenuHref || path === submenuHref + '/') {
                submenuLink.classList.add('active-submenu');
                // Ensure the main menu item is also highlighted
                dropdown.querySelector('a').classList.add('active-menu');
                console.log('Submenu active:', submenuHref); // Debugging: Log active submenu
            }
        });
    });
});


function copyToClipboard(text, labelId) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copied to clipboard: ' + text);
        const label = document.getElementById(labelId);
        label.innerHTML = 'Copied!<img src="/cs-assets/copy.svg" alt="Copy">';
        setTimeout(() => {
            label.innerHTML = 'Copy<img src="/cs-assets/copy.svg" alt="Copy">';
        }, 2000);
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

function switchMode() {
    window.location.href = 'https://aops-ba.github.io/cs-java-summer';
}