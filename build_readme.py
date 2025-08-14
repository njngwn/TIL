import os
import re
from datetime import datetime

# Folders to ignore
IGNORE_FOLDERS = ['.git', '.github']
# The temporary filename for new TILs
TEMP_TIL_FILENAME = "til.md"
# The root README file
ROOT_README_FILE = "README.md"

def slugify(text):
    """
    Converts text into a URL/filename-friendly 'slug'.
    Example: "My Awesome Title!!" -> "my-awesome-title"
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text

def rename_temp_til_file():
    """
    Finds a 'til.md' file and renames it based on its first H1 tag.
    """
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        if TEMP_TIL_FILENAME in files:
            temp_filepath = os.path.join(root, TEMP_TIL_FILENAME)

            with open(temp_filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()

            if first_line.startswith('# '):
                title = first_line.replace('# ', '').strip()
                new_filename = f"{slugify(title)}.md"
                new_filepath = os.path.join(root, new_filename)

                if os.path.exists(new_filepath):
                    print(f"Warning: '{new_filepath}' already exists. Skipping rename.")
                    return

                os.rename(temp_filepath, new_filepath)
                print(f"Renamed '{temp_filepath}' to '{new_filepath}'")
                return

# --- Main Logic ---
rename_temp_til_file()

til_entries = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

    for file in files:
        if file.endswith(".md") and file != ROOT_README_FILE and file != TEMP_TIL_FILENAME:
            filepath = os.path.join(root, file)
            mtime = os.path.getmtime(filepath)
            date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            web_filepath = filepath.replace(os.path.sep, '/')
            entry = f"* [{web_filepath}]({web_filepath}) - {date_str}"
            til_entries.append((mtime, entry))

til_entries.sort(key=lambda x: x[0], reverse=True)
tils_markdown = "\n".join([entry for _, entry in til_entries])

with open(ROOT_README_FILE, "r", encoding="utf-8") as f:
    readme_content = f.read()

new_readme = re.sub(
    r"(.|\n)*",
    f"\n{tils_markdown}\n",
    readme_content
)

with open(ROOT_README_FILE, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README.md has been updated successfully!")