from PIL import Image, ImageTk
from tkinter import PhotoImage
import os


# full_filename maps to PhotoImage
_image_cache: dict[str, PhotoImage] = {}


def get_image(query_fn) -> PhotoImage:
    """You do not need to supply a file extension, only the filename.
    Tries to get the image from the cached images before loading from disk"""
    img_dir = os.path.join('.', 'data', 'img')

    def get_full_filename():
        # use the query_fn to match to a full filename in the img folder
        for fn in os.listdir(img_dir):
            if query_fn in fn:
                return fn
        else:
            raise FileNotFoundError(f'Could find image matching "{query_fn}"')

    def load_image():
        file_path = os.path.join(img_dir, get_full_filename())
        # try to load from cache dict or load from disk

        if img := _image_cache.get(file_path):
            return img
        else:
            img = ImageTk.PhotoImage(Image.open(file_path))
            _image_cache.update({file_path: img})
            return img

    return load_image()
