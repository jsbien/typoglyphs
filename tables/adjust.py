import os
import re
import shutil

input_directory = 'glyphs'

# Regex pattern to match filenames like 't12_glyphs.tex'
filename_pattern = re.compile(r'^t(\d{2})_glyphs\.tex$')

for filename in os.listdir(input_directory):
    match = filename_pattern.match(filename)
    if match:
        number = match.group(1)
        filepath = os.path.join(input_directory, filename)
        backup_path = filepath + '.bak'

        # Create a backup
        shutil.copy(filepath, backup_path)

        # Read, replace, and write back
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        new_content = content.replace('{5}', f'{{{number}}}')
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f'Processed {filename}: {{5}} → {{{number}}}, backup saved as {filename}.bak')
