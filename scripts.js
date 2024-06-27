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
        if (path.includes(menuLink)) {
            dropdown.querySelector('a').classList.add('active-menu');
            console.log('Main menu active:', menuLink); // Debugging: Log active main menu
        }

        // Check if any submenu item should be active
        submenuLinks.forEach(submenuLink => {
            const submenuHref = submenuLink.getAttribute('href').toLowerCase().replace('\\', '/');
			console.log('Sub:', submenuHref);

            if (path.includes(submenuHref)) {
                submenuLink.classList.add('active-submenu');
                // Ensure the main menu item is also highlighted
                dropdown.querySelector('a').classList.add('active-menu');
                console.log('Submenu active:', submenuHref); // Debugging: Log active submenu
            }
        });
    });
});