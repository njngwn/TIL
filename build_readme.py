import os
import re
from datetime import datetime

# --- Configuration ---
# Folders to ignore when searching for TILs
IGNORE_FOLDERS = ['.git', '.github']
# The temporary filename for new TILs
TEMP_TIL_FILENAME = "til.md"
# The root README file to update
ROOT_README_FILE = "README.md"
# The placeholder markers in the README file
START_MARKER = ""
END_MARKER = ""

def slugify(text):
    """
    Converts a string into a URL/filename-friendly 'slug'.
    Example: "My Awesome Title!!" -> "my-awesome-title"
    """
    # Convert to lowercase
    text = text.lower()
    # Remove characters that are not alphanumeric, spaces, or hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces or consecutive hyphens with a single hyphen
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text

def rename_temp_til_file():
    """
    Finds a file named 'til.md', reads its first line for an H1 title,
    and renames the file based on that title.
    """
    for root, dirs, files in os.walk("."):
        # Prune the directory search to ignore specified folders
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        
        if TEMP_TIL_FILENAME in files:
            temp_filepath = os.path.join(root, TEMP_TIL_FILENAME)
            
            with open(temp_filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            
            # Check if the first line is a valid H1 markdown heading
            if first_line.startswith('# '):
                title = first_line.replace('# ', '').strip()
                if not title:
                    print(f"Warning: Title in '{temp_filepath}' is empty. Skipping rename.")
                    return

                new_filename = f"{slugify(title)}.md"
                new_filepath = os.path.join(root, new_filename)
                
                # To prevent overwriting, skip if a file with the new name already exists
                if os.path.exists(new_filepath):
                    print(f"Warning: '{new_filepath}' already exists. Skipping rename.")
                    return

                os.rename(temp_filepath, new_filepath)
                print(f"Renamed '{temp_filepath}' to '{new_filepath}'")
                # Process only the first 'til.md' found and then exit the function
                return

# --- Main Logic ---

# 1. First, try to rename a temporary TIL file if one exists.
rename_temp_til_file()

# 2. Next, scan all directories to build the table of contents.
til_entries = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

    for file in files:
        # Include only markdown files, excluding the main README and any temporary files
        if file.endswith(".md") and file != ROOT_README_FILE and file != TEMP_TIL_FILENAME:
            filepath = os.path.join(root, file)
            mtime = os.path.getmtime(filepath)
            date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            
            # Normalize file path to use web-friendly forward slashes for the link
            web_filepath = filepath.replace(os.path.sep, '/')
            # Create the markdown list item for the TOC
            entry = f"* [{web_filepath}]({web_filepath}) - {date_str}"
            til_entries.append((mtime, entry))

# Sort entries by modification time, newest first
til_entries.sort(key=lambda x: x[0], reverse=True)
tils_markdown = "\n".join([entry for _, entry in til_entries])

# 3. Finally, update the main README.md file.
try:
    with open(ROOT_README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Use regex to find the content between the start and end markers
    # The re.DOTALL flag allows '.' to match newlines
    new_readme = re.sub(
        f"{START_MARKER}(.|\n)*{END_MARKER}",
        f"{START_MARKER}\n{tils_markdown}\n{END_MARKER}",
        readme_content
    )

    # Write the updated content back to the README file
    with open(ROOT_README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md has been updated successfully!")

except FileNotFoundError:
    print(f"Error: {ROOT_README_FILE} not found. Please create it first.")