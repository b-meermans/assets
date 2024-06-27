import os
import re

def generate_html(folder_path):
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
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <h1>Image Previews</h1>
    <div class="menu-container">
        <div class="menu">
            <div class="dropdown">
                <a href="/Boardgames/">Boardgames</a>
                <div class="dropdown-content">
                    <a href="/Boardgames/Dice/index.html">Dice</a>
                    <a href="/Boardgames/Pieces/index.html">Pieces</a>
                    <a href="/Boardgames/PlayingCards/index.html">Playing Cards</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/Characters/">Characters</a>
                <div class="dropdown-content">
                    <a href="/Characters/Heroes/index.html">Heroes</a>
                    <a href="/Characters/Villains/index.html">Villains</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/General/">General</a>
                <div class="dropdown-content">
                    <a href="/General/Item1/index.html">Item 1</a>
                    <a href="/General/Item2/index.html">Item 2</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/Landscape/">Landscape</a>
                <div class="dropdown-content">
                    <a href="/Landscape/Mountains/index.html">Mountains</a>
                    <a href="/Landscape/Rivers/index.html">Rivers</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/Original/">Original</a>
                <div class="dropdown-content">
                    <a href="/Original/Concepts/index.html">Concepts</a>
                    <a href="/Original/Designs/index.html">Designs</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/Symbols/">Symbols</a>
                <div class="dropdown-content">
                    <a href="/Symbols/Basic/index.html">Basic</a>
                    <a href="/Symbols/Complex/index.html">Complex</a>
                    <a href="/Symbols/SpeechBubbles/index.html">Speech Bubbles</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="/Transport/">Transport</a>
                <div class="dropdown-content">
                    <a href="/Transport/Cars/index.html">Cars</a>
                    <a href="/Transport/Planes/index.html">Planes</a>
                </div>
            </div>
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
    <script src="/scripts.js"></script>
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
    generate_html(subdir)
