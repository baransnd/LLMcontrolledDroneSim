import os
import subprocess

# Directory containing .ui files
source_dir = "../QtUiProjekt"

# Directory to output .py files
output_dir = "../UI_Windows_Form"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get list of .ui files
ui_files = [f for f in os.listdir(source_dir) if f.endswith('.ui')]

# Compile each .ui file to a .py file
for ui_file in ui_files:
    py_file = f"{os.path.splitext(ui_file)[0]}.py"
    source_file = os.path.join(source_dir, ui_file)
    output_file = os.path.join(output_dir, py_file)

    # Use either 'pyuic6' or 'pyside6-uic' depending on your PyQt version
    # subprocess.run(['pyuic6', source_file, '-o', output_file])
    subprocess.run(['pyside6-uic', source_file, '-o', output_file])
