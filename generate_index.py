import os
import re

def generate_html(folder_path, root_directory, menu_html):
    readme_path = os.path.join(folder_path, 'readme.md')
    index_path = os.path.join(folder_path, 'index.html')

    if not os.path.exists(readme_path):
        print(f"readme.md not found in {folder_path}")
        return

    # Read the markdown file
    with open(readme_path, 'r') as file:
        content = file.read()

    # Extract image entries using regex
    image_entries = re.findall(r'<img src="([^"]+)" width="100" /> ([^<]+)<br>', content)

    # Generate HTML content
    html_content = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Previews</title>
        <link rel="stylesheet" href="/cs-assets/styles.css">
        <link rel="icon" href="/cs-assets/favicon.ico" type="image/x-icon"> <!-- Favicon link -->
    </head>
    <body>
        <div class="content-container">
            <div class="menu-container">
                <div class="menu">
    {menu_html}
                </div>
            </div>
            <div class="image-grid">
    '''

    for idx, (src, alt) in enumerate(image_entries):
        filename = os.path.basename(src)
        html_content += f'''
                <div class="image-cell" onclick="copyToClipboard('{filename}', 'copy-label-{idx}')">
                    <div class="image-container">
                        <img src="{src}" alt="{alt}">
                    </div>
                    <div class="copy-label" id="copy-label-{idx}">Copy<img src="/cs-assets/copy.svg" alt="Copy"></div>
                    <div class="image-label">{alt}</div>
                </div>
        '''

    html_content += '''
            </div>
        </div>
        <script src="/cs-assets/scripts.js"></script>
        <script>
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
        </script>
    </body>
    </html>
    '''

    # Write the HTML content to index.html
    with open(index_path, 'w') as file:
        file.write(html_content)

    print(f"Generated {index_path}")



def generate_menu_html(root_directory):
    menu_html = ""
    directories = next(os.walk(root_directory))[1]
    
    # Sort directories alphabetically
    directories.sort()
    
    # Place "Original" folder at the beginning
    if "Original" in directories:
        directories.remove("Original")
        directories.insert(0, "Original")
    
    # Generate menu items dynamically
    for dirname in directories:
        if dirname.startswith('.'):
            continue  # Skip hidden folders
        relative_dir = os.path.relpath(os.path.join(root_directory, dirname), root_directory).replace('\\', '/')
        link_path = f"/cs-assets/{relative_dir}/index.html"
        
        # Change the display name of "Original" to "Theater"
        display_name = "Theater" if dirname == "Original" else dirname
        
        menu_html += f'''
            <div class="dropdown">
                <a href="{link_path}">{display_name}</a>
                <div class="dropdown-content">
'''
        # Generate sub-menu items for the immediate subdirectories only
        subdir_path = os.path.join(root_directory, dirname)
        subdirs = next(os.walk(subdir_path))[1]
        
        # Sort subdirectories alphabetically
        subdirs.sort()
        
        for subdirname in subdirs:
            if subdirname.startswith('.'):
                continue  # Skip hidden folders
            sub_relative_dir = os.path.relpath(os.path.join(subdir_path, subdirname), root_directory).replace('\\', '/')
            sub_link_path = f"/cs-assets/{sub_relative_dir}/index.html"
            menu_html += f'                    <a href="{sub_link_path}">{subdirname}</a>\n'

        menu_html += '''
                </div>
            </div>
'''
    return menu_html

# Path to the root directory containing the folders
root_directory = './'

# Generate the menu HTML once
menu_html = generate_menu_html(root_directory)

# Recursively process each folder and subfolder, excluding hidden ones
for subdir, dirs, _ in os.walk(root_directory):
    # Exclude hidden folders
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    generate_html(subdir, root_directory, menu_html)
