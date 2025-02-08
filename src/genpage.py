import os

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
    """
    Recursively crawls through the content directory.
    For each markdown (.md) file found, generate a corresponding .html file using the given template.
    The generated pages will be placed in the destination directory with the same directory structure.
    """
    file_names_in_content = os.listdir(dir_path_content)
    print(f"Listing files in {dir_path_content}: {file_names_in_content}")

    for file in file_names_in_content:
        source_path = os.path.join(dir_path_content, file)

        if os.path.isfile(source_path) and file.endswith(".md"):
            # Change extension to .html
            html_file_name = file.replace(".md", ".html")

            # Construct the destination file path
            dest_file_path = os.path.join(dest_dir_path, html_file_name)

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

            # Generate the HTML page
            generate_page(source_path, template_path, dest_file_path)
            print(f"Generated page: {dest_file_path}")

        elif os.path.isdir(source_path):
            # Create corresponding subdirectory in the destination
            new_dest_dir = os.path.join(dest_dir_path, file)
            os.makedirs(new_dest_dir, exist_ok=True)

            # Recurse into subdirectory
            generate_pages_recursive(source_path, template_path, new_dest_dir)
