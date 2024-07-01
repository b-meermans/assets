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

let imageFilenames = [];

fetch('/cs-assets/image_list.json')
    .then(response => response.json())
    .then(data => {
        imageFilenames = data;
    });

document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    const path = window.location.pathname.toLowerCase().replace('\\', '/');

    // Highlight the active menu and submenu items
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const menuLink = dropdown.querySelector('a').getAttribute('href').toLowerCase();
        const submenuLinks = dropdown.querySelectorAll('.dropdown-content a');


        // Check if the main menu item should be active
        if (path === menuLink || path === menuLink + '/') {
            dropdown.querySelector('a').classList.add('active-menu');
        }

        // Check if any submenu item should be active
        submenuLinks.forEach(submenuLink => {
            const submenuHref = submenuLink.getAttribute('href').toLowerCase().replace('\\', '/');

            if (path === submenuHref || path === submenuHref + '/') {
                submenuLink.classList.add('active-submenu');
                dropdown.querySelector('a').classList.add('active-menu');
            }
        });
    });

    const searchBar = document.getElementById('search-bar');
    const suggestions = document.getElementById('suggestions');

	searchBar.addEventListener('input', function() {
		const query = searchBar.value.toLowerCase();
		suggestions.innerHTML = '';

		if (query) {
			const filteredImages = imageFilenames.filter(image => 
				image.filename.toLowerCase().includes(query)
			);

			filteredImages.forEach(image => {
				const suggestionItem = document.createElement('div');
				suggestionItem.classList.add('suggestion-item');
				suggestionItem.innerHTML = `
					<span>${image.filename}</span>
					<img src="/${image.path}" class="preview-image" alt="${image.filename}">
				`;
				suggestionItem.addEventListener('click', () => {
					copyToClipboard(image.filename);
					const copiedLabel = document.createElement('div');
					copiedLabel.className = 'copied-label';
					copiedLabel.textContent = 'Copied!';
					suggestionItem.insertBefore(copiedLabel, suggestionItem.querySelector('.preview-image'));
					
					setTimeout(() => {
						copiedLabel.classList.add('show-copied');
					}, 100); // Slight delay to trigger transition

					setTimeout(() => {
						suggestionItem.removeChild(copiedLabel);
					}, 2000);
				});

				suggestions.appendChild(suggestionItem);
			});
			suggestions.style.display = 'block';
			suggestions.classList.add('visible');
		} else {
			suggestions.style.display = 'none';
			suggestions.classList.remove('visible');
		}
	});

    document.addEventListener('click', function(event) {
        if (!searchBar.contains(event.target) && !suggestions.contains(event.target)) {
            suggestions.style.display = 'none';
			suggestions.classList.remove('visible');
        }
    });

    searchBar.addEventListener('focus', function() {
        if (searchBar.value) {
            suggestions.style.display = 'block';
			suggestions.classList.add('visible');
        }
    });

    document.querySelector('.menu-container').addEventListener('mouseenter', function() {
        suggestions.style.display = 'none';
		suggestions.classList.remove('visible');
    });

    searchBar.addEventListener('click', function() {
        const input = this.value.toLowerCase();
        if (input) {
            suggestions.style.display = 'block';
			suggestions.classList.add('visible');
        }
    });
});

function copyToClipboard(text, labelId) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copied to clipboard: ' + text);
        const label = document.getElementById(labelId);
        label.innerHTML = 'Copied<img src="/cs-assets/copy.svg" alt="Copy">';
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
