import os
from os import replace

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    if "# " not in markdown:
        raise Exception("There is no title")
    return markdown[2:]


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from { from_path } to { dest_path } using { template_path }"
    )

    with open(from_path, "r") as f:
        from_content = f.read()
        title = extract_title(from_content)
        html = markdown_to_html_node(from_content).to_html()

    with open(template_path, "r") as f:
        temp_content = f.read()

    page_content = temp_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_content)

    print(f"Page successfully generated at {dest_path}")

    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        with open(dir_path_content, "r") as f:
            content_dir = f.read()
