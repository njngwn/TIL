import os
import re
from collections import defaultdict

# --- Configuration ---
# Folders to ignore when searching for TILs
IGNORE_FOLDERS = ['.git', '.github']
# The root README file to update
ROOT_README_FILE = "README.md"
# The placeholder markers in the README file
START_MARKER = ""
END_MARKER = ""

# --- Main Logic ---

# Use a dictionary to group TILs by their category (folder name)
# defaultdict simplifies this by automatically creating a list for new categories
tils_by_category = defaultdict(list)

# Scan all directories to find markdown files
for root, dirs, files in os.walk("."):
    # Prune the directory search to ignore specified folders
    dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

    for file in files:
        # Include only markdown files, excluding the main README
        if file.endswith(".md") and file != ROOT_README_FILE:
            filepath = os.path.join(root, file)
            
            # Get the category name from the parent directory
            # os.path.dirname gets the folder path, os.path.basename gets the last part
            category = os.path.basename(os.path.dirname(filepath))
            
            # If the file is in the root directory, use a default category name
            if category == ".":
                category = "General"
                
            # Add the file path to the correct category list
            tils_by_category[category].append(filepath)

# --- Generate the new Markdown content ---
tils_markdown = ""
# Sort categories alphabetically for consistent order
for category in sorted(tils_by_category.keys()):
    # Add the category as a subheading
    tils_markdown += f"### {category}\n"
    
    # Sort files alphabetically within each category
    for filepath in sorted(tils_by_category[category]):
        # Get just the filename for the link text
        filename = os.path.basename(filepath)
        # Normalize file path to use web-friendly forward slashes for the link
        web_filepath = filepath.replace(os.path.sep, '/')
        # Create the markdown list item
        tils_markdown += f"* [{filename}]({web_filepath})\n"
    
    # Add a blank line between categories for better readability
    tils_markdown += "\n"


# --- Update the README.md file ---
try:
    with open(ROOT_README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Use regex to find and replace the content between the markers
    new_readme = re.sub(
        f"{START_MARKER}(.|\n)*{END_MARKER}",
        f"{START_MARKER}\n{tils_markdown.strip()}\n{END_MARKER}",
        readme_content
    )

    # Write the updated content back to the README file
    with open(ROOT_README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md has been updated successfully with categorized list!")

except FileNotFoundError:
    print(f"Error: {ROOT_README_FILE} not found. Please create it first.")