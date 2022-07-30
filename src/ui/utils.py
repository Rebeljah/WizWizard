from PIL import Image, ImageTk
from tkinter import PhotoImage
from pathlib import Path


# full_filename maps to PhotoImage
IMG_CACHE: dict[str, PhotoImage] = {}
IMG_DIR = Path(__file__).parent.parent / 'img'


def get_image(partial_filename) -> PhotoImage:
    """You do not need to supply a file extension, only the filename.
    Tries to get the image from the cached images before loading from disk"""

    def get_full_filepath() -> Path:
        # use the query_fn to match to a full filename in the img folder
        for path in IMG_DIR.iterdir():
            if partial_filename in path.name:
                return path
        else:
            raise FileNotFoundError(f'Could find image matching "{partial_filename}"')

    def load_image(path: Path):
        # try to load from cache dict or load from disk
        if img := IMG_CACHE.get(path):
            return img
        else:
            img = ImageTk.PhotoImage(Image.open(path))
            IMG_CACHE[path] = img
            return img

    return load_image(get_full_filepath())
