import os
import shutil

def copy_static_to_public_caller():
    public_path = os.path.abspath("public/")
    shutil.rmtree(public_path)

    os.mkdir("./public")

    static_path = os.path.abspath("static/")
    copy_static_to_public(static_path)

def copy_static_to_public(directory):
    list_dir = os.listdir(directory)
    for item in list_dir:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            new_dir = item_path.replace('static/', 'public/')
            print(f"making new directory at: {new_dir}")
            os.mkdir(new_dir)
            copy_static_to_public(item_path)
        else:
            item_new_path = item_path.replace("static/", "public/")
            print(f"making new file at: {item_new_path}")
            shutil.copy(item_path, item_new_path)




def main():
    copy_static_to_public_caller()


if __name__ == "__main__":
    main()