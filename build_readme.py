import os
import re
from datetime import datetime

ignore_folders = ['.git', '.github']
root_readme_file = "README.md"

til_entries = []

# explore all directories
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ignore_folders]

    for file in files:
        if file.endswith(".md") and file != root_readme_file:
            filepath = os.path.join(root, file)
            # get last modified time
            mtime = os.path.getmtime(filepath)
            # convert time format
            date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            # convert to markdown link
            entry = f"* [{filepath}]({filepath}) - {date_str}"
            til_entries.append((mtime, entry))

# order by time
til_entries.sort(key=lambda x: x[0], reverse=True)

# generate lists
tils_markdown = "\n".join([entry for _, entry in til_entries])

with open(root_readme_file, "r", encoding="utf-8") as f:
    readme_content = f.read()

new_readme = re.sub(
    r"(.|\n)*",
    f"\n{tils_markdown}\n",
    readme_content
)

with open(root_readme_file, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README.md has been updated successfully!")