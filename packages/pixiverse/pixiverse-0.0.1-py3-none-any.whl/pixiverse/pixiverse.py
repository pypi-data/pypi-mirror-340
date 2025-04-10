import cv2
import pillow_heif
import pillow_avif
from pillow_heif import register_heif_opener
import numpy as np
from PIL import Image
import os
import io
import PIL.Image
from typing import Union, List, Tuple

register_heif_opener(decode_threads=1, thumbnails=True)
pillow_heif.options.THUMBNAILS = True
pillow_heif.options.DECODE_THREADS = 1


def get_image_format(filename: str) -> str:
    try:
        with Image.open(filename) as img:
            return img.format.lower()
    except IOError:
        return "unknown"


def save_heif(file: str, img: Union[np.ndarray, PIL.Image]):
    modes = {
        4: "BGRA",
        3: "BGR",
        1: "L"
    }
    channels = 1 if len(img.shape) == 2 else img.shape[-1]
    if isinstance(img, PIL.Image.Image):
        if channels == 1:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
        elif channels == 3:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        elif channels == 4:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    mode = modes[channels]
    w, h = img.shape[1], img.shape[0]
    heif_file = pillow_heif.from_bytes(mode=mode, size=(w, h), data=bytes(img))
    heif_file.save(file, quality=-1)


def save_avif(file: str, img: Union[np.ndarray, PIL.Image]):
    if isinstance(img, np.ndarray):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
    img.save(file, "AVIF")


def save_opencv(file: str, img: np.ndarray):
    def imwrite_ex(filename, img, params=None):
        r, eimg = cv2.imencode(os.path.splitext(filename)[1], img, params)
        if r:
            with open(filename, mode="wb") as f:
                eimg.tofile(f)
        return r

    ext = os.path.splitext(file)[1]
    if ext == ".webp" and img.shape[-1] == 4:
        cv2.imwrite(file, img)
    # elif ext == ".exr":
    #     cv2.imwrite(file, img.astype(np.float32))
    elif ext in [".pgm"]:
        if len(img.shape) == 3 and img.shape[2] == 3:
            cv2.imwrite(file, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    else:
        imwrite_ex(file, img)


def save_pillow(file: str, img: PIL.Image):
    img.save(file, format=None)


def load_heif(file: str) -> np.ndarray:
    heif_file = pillow_heif.open_heif(file, convert_hdr_to_8bit=False, bgr_mode=True)
    img = np.array(heif_file)
    return img


def load_opencv(file: str) -> np.ndarray:
    return cv2.imread(file, cv2.IMREAD_UNCHANGED)


def imwrite(file: str, img: Union[np.ndarray, PIL.Image]):
    ext = os.path.splitext(file)[0][1:]
    if ext in ["heif", "heic"]:
        return save_heif(file, img)
    if ext in ["avif"]:
        return save_avif(file, img)
    if isinstance(img, np.ndarray):
        return save_opencv(file, img)
    if isinstance(img, PIL.Image):
        return save_pillow(file, img)


def imread(file: str):
    fmt = get_image_format(file)
    if fmt in ["heif", "heic", "avif"]:
        return load_heif(file)
    if fmt in ["webp", "png", "jpg", "bmp", "pgm", "jpeg"]:
        return load_opencv(file)
