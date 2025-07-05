import os
import shutil
import filetype

# Set this to your decrypted files folder
SOURCE_FOLDER = r"\Encoded_discord\Cache_Data"

# Where to store organized files
DEST_BASE = os.path.join(SOURCE_FOLDER, "organized")

# Mapping extensions to folder names
EXTENSION_MAP = {
    "jpg": "images",
    "jpeg": "images",
    "png": "images",
    "webp": "images",
    "gif": "images",
    "woff2": "fonts",
    "ttf": "fonts",
    "otf": "fonts",
    "gz": "compressed",
    "zip": "compressed",
    "json": "data",
    "html": "web",
    "js": "web",
    "css": "web"
}

# Make folders
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def organize():
    ensure_folder(DEST_BASE)
    for filename in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, filename)
        if not os.path.isfile(file_path):
            continue

        kind = filetype.guess(file_path)
        if kind:
            ext = kind.extension
            new_name = filename.split(".")[0] + "." + ext
            folder = EXTENSION_MAP.get(ext, "misc")
        else:
            ext = None
            new_name = filename
            folder = "unknown"

        dest_folder = os.path.join(DEST_BASE, folder)
        ensure_folder(dest_folder)
        dest_path = os.path.join(dest_folder, new_name)

        print(f"Moving {filename} → {folder}/{new_name}")
        shutil.copy2(file_path, dest_path)

if __name__ == "__main__":
    organize()
