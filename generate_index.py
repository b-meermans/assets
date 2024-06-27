import os
import re

def generate_html(folder_path, root_directory):
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
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Previews</title>
    <link rel="stylesheet" href="/cs-assets/styles.css">
</head>
<body>
    <div class="menu-container">
        <div class="menu">
'''

    # Generate menu items dynamically
    for dirpath, dirnames, _ in os.walk(root_directory):
        for dirname in dirnames:
            relative_dir = os.path.relpath(os.path.join(dirpath, dirname), root_directory)
            link_path = f"/cs-assets/{relative_dir}/index.html"
            html_content += f'''
            <div class="dropdown">
                <a href="{link_path}">{dirname}</a>
                <div class="dropdown-content">
'''
            # Generate sub-menu items dynamically
            for subdirpath, subdirnames, _ in os.walk(os.path.join(root_directory, relative_dir)):
                for subdirname in subdirnames:
                    sub_relative_dir = os.path.relpath(os.path.join(subdirpath, subdirname), root_directory)
                    sub_link_path = f"/cs-assets/{sub_relative_dir}/index.html"
                    html_content += f'                    <a href="{sub_link_path}">{subdirname}</a>\n'
                break  # Only process the top-level subdirectories

            html_content += '''
                </div>
            </div>
'''

    html_content += '''
        </div>
    </div>
    <div class="image-grid">
'''

    for src, alt in image_entries:
        html_content += f'''
        <div class="image-cell">
            <img src="{src}" alt="{alt}">
            <div class="image-label">{alt}</div>
        </div>
        '''

    html_content += '''
    </div>
    <script src="/cs-assets/scripts.js"></script>
</body>
</html>
'''

    # Write the HTML content to index.html
    with open(index_path, 'w') as file:
        file.write(html_content)

    print(f"Generated {index_path}")

# Path to the root directory containing the folders
root_directory = './'

# Recursively process each folder and subfolder, excluding hidden ones
for subdir, dirs, _ in os.walk(root_directory):
    # Exclude hidden folders
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    generate_html(subdir, root_directory)
