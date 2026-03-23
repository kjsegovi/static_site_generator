import os
import shutil
from src.markdown_to_html import markdown_to_html_node
from pathlib import Path
import sys

def copy_static_to_public_caller():
    public_path = os.path.abspath("docs/")
    try:
        shutil.rmtree(public_path)
    except FileNotFoundError:
        print("docs doesn't exists. skipping...")

    os.mkdir("./docs")

    static_path = os.path.abspath("static/")
    copy_static_to_public(static_path)

def copy_static_to_public(directory):
    list_dir = os.listdir(directory)
    for item in list_dir:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            new_dir = item_path.replace('static/', 'docs/')
            print(f"making new directory at: {new_dir}")
            try:
                os.mkdir(new_dir)
            except FileExistsError:
                print(f"Directory {new_dir} already exists. Skipping")
            except Exception as e:
                raise Exception(f"There was an issue with creating the directory. Error: {e}")
            copy_static_to_public(item_path)
        else:
            if item.endswith(".md"):
                continue
            item_new_path = item_path.replace("static/", "docs/")
            print(f"making new file at: {item_new_path}")
            try:
                shutil.copy(item_path, item_new_path)
            except FileExistsError:
                print(f"File {item_new_path}{item_path} already exists. Skipping")
            except Exception as e:
                raise Exception(f"There was an issue with creating the new file. Error: {e}")


def extract_title(markdown):
    # print(markdown.split())
    title = markdown.lstrip().split("\n")[0]
    if not title:
        raise Exception("There is no text in the markdown")

    checker = title[0:2]
    if checker != "# ":
        raise Exception("There is no title heading for this markdown")

    title = title[2:]
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating {from_path} to {dest_path} using {template_path}.")
    with open(from_path, 'r') as markdown_file:
        markdown_from_path = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_from_path = template_file.read()

    markdown_node = markdown_to_html_node(markdown_from_path)
    html_node = markdown_node.to_html()
    html_title = extract_title(markdown_from_path)
    template_from_path = template_from_path.replace("{{ Title }}", html_title)
    template_from_path = template_from_path.replace("{{ Content }}", html_node)
    template_from_path = template_from_path.replace('href="/', f'href="{basepath}')
    template_from_path = template_from_path.replace('src="/', f'src="{basepath}')
    # print(template_from_path)
    # check to see if the path file exists, doing it with pathlib...
    file_checker = Path(dest_path).expanduser()
    file_checker.parent.mkdir(parents=True, exist_ok=True)
    file_checker.write_text(template_from_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            # Recurse into subdirectory
            new_dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest, basepath)
        elif item.endswith(".md"):
            # Build the destination .html path
            html_filename = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(item_path, template_path, dest_path, basepath)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public_caller()
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()