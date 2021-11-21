from PIL import Image, ImageTk
from tkinter import PhotoImage
import os


# full_filename maps to PhotoImage
_image_cache: dict[str, PhotoImage] = {}


def get_image(query_fn) -> PhotoImage:
    """You do not need to supply a file extension, only the filename.
    Tries to get the image from the cached images before loading from disk"""
    def get_full_filename():
        # use the query_fn to match to a full filename in the img folder
        for fn in os.listdir("./img/"):
            if query_fn in fn:
                return fn
        else:
            raise FileNotFoundError(f'Could find image matching "{query_fn}"')

    file_path = os.path.join('./img/', get_full_filename())

    # try to load from cache dict or load from disk
    img = _image_cache.get(file_path)
    if not img:
        img = ImageTk.PhotoImage(Image.open(file_path))
        _image_cache.update({file_path: img})

    return img
