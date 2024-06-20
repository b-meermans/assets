import os
from PIL import Image
import argparse

# Function to convert filename to enum name
def filename_to_enum_name(filename):
    name_part = os.path.splitext(filename)[0]  # remove extension
    return name_part.replace("-", "_").upper()

# Template for the Java enum
java_enum_template = '''package AopsTheater;

import java.util.Map;
import java.util.HashMap;
import java.util.Optional;

public enum Image {{
{enum_values};

    private final String filename;
    private final int width;
    private final int height;
    private static final Map<String, Image> stringToImageMap = new HashMap<>();

    Image(String filename, int width, int height) {{
        this.filename = filename;
        this.width = width;
        this.height = height;
    }}

    public String getFilename() {{
        return filename;
    }}

    public int getWidth() {{
        return width;
    }}

    public int getHeight() {{
        return height;
    }}

    static {{
        for (Image image : Image.values()) {{
            stringToImageMap.put(image.getFilename(), image);
        }}
    }}

   static Optional<Image> getImageByFilename(String filename) {{
        return Optional.ofNullable(stringToImageMap.get(filename));
    }}
}}
'''

def generate_java_enum(directory, output_file):
    enum_values = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.png'):
                filepath = os.path.join(root, filename)
                with Image.open(filepath) as img:
                    width, height = img.size
                enum_name = filename_to_enum_name(filename)
                enum_values.append(f'    {enum_name}("{filename}", {width}, {height})')

    # Join all enum values into the final string
    enum_values_str = ',\n'.join(enum_values)

    # Generate the final Java enum code
    java_enum_code = java_enum_template.format(enum_values=enum_values_str)

    # Write the Java enum code to the output file
    with open(output_file, 'w') as f:
        f.write(java_enum_code)

def main():
    parser = argparse.ArgumentParser(description="Generate Java enum from image metadata.")
    parser.add_argument('-d', '--directory', type=str, required=True, help="Directory containing the images.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file for the generated Java enum.")
    
    args = parser.parse_args()
    
    generate_java_enum(args.directory, args.output)

if __name__ == '__main__':
    main()
