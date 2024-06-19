import os
import argparse

# Function to convert filename to variable name
def filename_to_variable_name(filename):
    name_part = os.path.splitext(filename)[0]  # remove extension
    components = name_part.split('-')
    return components[0] + ''.join(word.capitalize() for word in components[1:]) + 'Image'

# Function to walk through all files in a directory and its subdirectories
def walk_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            yield root, file

def generate_import_and_switch_case(directory, output_file):
    import_statements = []
    case_statements = []

    for root, filename in walk_directory(directory):
        if filename.endswith('.png'):
            relative_path = os.path.relpath(os.path.join(root, filename), directory)
            variable_name = filename_to_variable_name(filename)
            import_path = os.path.join('../../assets', relative_path).replace('\\', '/')  # Handle different OS path separators
            import_statements.append(f'import {variable_name} from "{import_path}";')
            case_statements.append(f'        case "{filename}":\n            image = {variable_name};\n            break;')

    # Join all import statements and case statements into their respective strings
    import_statements_str = '\n'.join(import_statements)
    case_statements_str = '\n'.join(case_statements)

    # Template for the final TypeScript code
    typescript_code_template = '''{imports}

export function mapFilenameToImageModule(filename: string): typeof aopsImage {{
    let image = aopsImage;
    switch (filename) {{
{cases}
        default:
            console.log("Unknown image", filename);
            break;
    }}
    return image;
}}
'''

    # Generate the final TypeScript code
    typescript_code = typescript_code_template.format(imports=import_statements_str, cases=case_statements_str)

    # Write the TypeScript code to the output file
    with open(output_file, 'w') as f:
        f.write(typescript_code)

def main():
    parser = argparse.ArgumentParser(description="Generate TypeScript import and switch-case statements from image filenames.")
    parser.add_argument('-d', '--directory', type=str, required=True, help="Directory containing the images.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file for the generated TypeScript code.")
    
    args = parser.parse_args()
    
    generate_import_and_switch_case(args.directory, args.output)

if __name__ == '__main__':
    main()
