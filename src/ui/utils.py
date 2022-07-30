from PIL import Image, ImageTk
from tkinter import PhotoImage
import os
from pathlib import Path


# full_filename maps to PhotoImage
IMG_CACHE: dict[str, PhotoImage] = {}
IMG_DIR = Path(__file__).parent.parent / 'img'


def get_image(partial_filename) -> PhotoImage:
    """You do not need to supply a file extension, only the filename.
    Tries to get the image from the cached images before loading from disk"""

    def get_full_filepath():
        # use the query_fn to match to a full filename in the img folder
        for full_filename in os.listdir(IMG_DIR):
            if partial_filename in full_filename:
                return Path(IMG_DIR) / full_filename
        else:
            raise FileNotFoundError(f'Could find image matching "{partial_filename}"')

    def load_image(file_path):
        # try to load from cache dict or load from disk
        if img := IMG_CACHE.get(file_path):
            return img
        else:
            img = ImageTk.PhotoImage(Image.open(file_path))
            IMG_CACHE[file_path] = img
            return img

    return load_image(get_full_filepath())
