import os
import re
import json

def generate_image_list(root_directory):
    image_list = []
    for folder_path, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                rel_path = os.path.relpath(folder_path, root_directory).replace('\\', '/')
                image_list.append({
                    'path': f"{rel_path}/{file}",
                    'filename': file
                })
    return image_list

def write_image_list_to_json(root_directory):
    image_list = generate_image_list(root_directory)
    with open(os.path.join(root_directory, 'image_list.json'), 'w', encoding='utf-8') as f:
        json.dump(image_list, f)

def generate_html(folder_path, root_directory, menu_html):
    readme_path = os.path.join(folder_path, 'readme.md')
    index_path = os.path.join(folder_path, 'index.html')

    if not os.path.exists(readme_path):
        print(f"readme.md not found in {folder_path}")
        return

    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    image_entries = re.findall(r'<img src="([^"]+)" width="100" /> ([^<]+)<br>', content)

    title = 'Assets: ' + os.path.relpath(folder_path, root_directory).replace(os.sep, '-')

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link rel="stylesheet" href="/cs-assets/styles.css">
            <link rel="icon" href="/cs-assets/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <div class="content-container">
                <div class="menu-container">
                    <div class="menu">
        {menu_html}
                    </div>
                </div>
                <div class="search-container">
                    <input type="text" id="search-bar" placeholder="Search images...">
                    <div id="suggestions" class="suggestions-list"></div>
                </div>
                <div class="image-grid">
    '''

    for index, (src, alt) in enumerate(image_entries):
        filename = os.path.basename(src)
        label_id = f'copy-label-{index}'
        html_content += f'''
                    <div class="image-cell" onclick="copyToClipboard('{filename}', '{label_id}')">
                        <div class="image-container">
                            <img src="{src}" alt="{alt}">
                        </div>
                        <div class="copy-label" id="{label_id}">Copy <img src="/cs-assets/copy.svg" alt="Copy"></div>
                        <div class="image-label">{alt}</div>
                    </div>
        '''

    html_content += '''
                </div>
            </div>
            <button class="floating-button" onclick="switchMode()">🔁 Docs</button>
            <script src="/cs-assets/scripts.js"></script>
            <script src="/cs-assets/image_list.json"></script>
        </body>
        </html>
    '''

    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"Generated {index_path}")

def generate_menu_html(root_directory):
    menu_html = ""
    directories = next(os.walk(root_directory))[1]
    
    directories.sort()
    
    if "Original" in directories:
        directories.remove("Original")
        directories.insert(0, "Original")
    
    for dirname in directories:
        if dirname.startswith('.'):
            continue
        relative_dir = os.path.relpath(os.path.join(root_directory, dirname), root_directory).replace('\\', '/')
        link_path = f"/cs-assets/{relative_dir}/index.html"
        
        display_name = "Theater" if dirname == "Original" else dirname
        
        menu_html += f'''
            <div class="dropdown">
                <a href="{link_path}">{display_name}</a>
                <div class="dropdown-content">
'''
        subdir_path = os.path.join(root_directory, dirname)
        subdirs = next(os.walk(subdir_path))[1]
        
        subdirs.sort()
        
        for subdirname in subdirs:
            if subdirname.startswith('.'):
                continue
            sub_relative_dir = os.path.relpath(os.path.join(subdir_path, subdirname), root_directory).replace('\\', '/')
            sub_link_path = f"/cs-assets/{sub_relative_dir}/index.html"
            menu_html += f'                    <a href="{sub_link_path}">{subdirname}</a>\n'

        menu_html += '''
                </div>
            </div>
'''
    return menu_html

root_directory = './'

menu_html = generate_menu_html(root_directory)

write_image_list_to_json(root_directory)

for subdir, dirs, _ in os.walk(root_directory):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    generate_html(subdir, root_directory, menu_html)
