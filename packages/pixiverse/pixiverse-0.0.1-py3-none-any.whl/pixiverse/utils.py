import os
import cv2
import numpy as np
from typing import *
import base64
import io
from PIL import Image
import urllib.request


def from_blank(width: int, height: int, BGR: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    return np.zeros((height, width, 3), dtype=np.uint8) + np.array(BGR, dtype=np.uint8)


def from_url(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        image_data = response.read()
        image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:  # gif일 경우
            gif = Image.open(io.BytesIO(image_data))
            gif.seek(0)
            image = np.array(gif.convert('RGB'))
        return image
    except Exception as e:
        print(e)
        return None


def from_pil(img_pil):
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def from_base64(b64str: str):
    img = Image.open(io.BytesIO(base64.b64decode(b64str)))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)


def from_bytes(img_bytes):
    return cv2.cvtColor(np.array(Image.open(io.BytesIO(img_bytes))), cv2.COLOR_RGB2BGR)


def to_base64(img: np.ndarray, ext: str = ".png", params=None):
    return base64.b64encode(cv2.imencode(ext, img, params)[1]).decode("utf-8")


def to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def to_bytes(img: np.ndarray, ext: str = ".png"):
    return cv2.imencode(ext, img)[1].tobytes()


def to_color(img: np.ndarray):
    if len(img.shape) == 2 or img.shape[2] == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def resize(img: np.ndarray, width=None, height=None, interpolation=cv2.INTER_AREA, return_size=False):
    """
    Given both width and height, choose the smaller of the resulting sizes.
    :param img: opencv image
    :param width: width to change
    :param height: height to change
    :param interpolation: interpolation
    :return: opencv image
    """
    h, w = img.shape[:2]
    dims = []
    if height is not None:
        ratio = height / h
        dims.append((int(w * ratio), height))
    if width is not None:
        ratio = width / w
        dims.append((width, int(h * ratio)))
    if len(dims) == 2 and dims[0] > dims[1]:
        dims = dims[1:]
    if len(dims) == 0:
        return img if not return_size else (w, h)

    return cv2.resize(img, dims[0], interpolation=interpolation) if not return_size else dims[0]


def overlay(bgimg3c: np.ndarray, fgimg4c: np.ndarray, coord=(0, 0), inplace=True):
    """
    Overlay a 4-channel image on a 3-channel image
    :param bgimg3c: background 3c image
    :param fgimg4c: foreground 4c image
    :param coord: Coordinates of the bgimg3c  to overlay
    :param inplace: If true, bgimg3c is changed
    :return: Overlaid image
    """
    # if bgimg3c.shape[:2] != fgimg4c.shape[:2]:
    #     raise ValueError(bgimg3c.shape[:2], fgimg4c.shape[:2])
    h, w = fgimg4c.shape[:2]
    crop = bgimg3c[coord[0]:coord[0] + h, coord[1]:coord[1] + w]
    b, g, r, a = cv2.split(fgimg4c)
    mask = cv2.merge([a, a, a])
    fgimg3c = cv2.merge([b, g, r])
    mask = mask / 255.0
    mask_inv = 1.0 - mask
    ret = (crop * mask_inv + fgimg3c * mask).clip(0, 255).astype(np.uint8)
    if inplace:
        bgimg3c[coord[0]:coord[0] + h, coord[1]:coord[1] + w] = ret
    return ret


def center_pad(img: np.ndarray, width: int, height: int, value: Any = 33):
    """
    Places an image at the size you specify, centered and keep ratio.
    :param img: opencv image
    :param width: width
    :param height: height
    :param value: pad value(int or tuple)
    :return: opencv image
    """
    channel = 1 if len(img.shape) == 2 else img.shape[2]
    if isinstance(value, int):
        value = tuple([value] * channel)
    dst = np.zeros((height, width, channel), dtype=np.uint8) + np.array(value, dtype=np.uint8)
    dx = (dst.shape[1] - img.shape[1]) // 2
    dy = (dst.shape[0] - img.shape[0]) // 2
    dst[dy:dy + img.shape[0], dx:dx + img.shape[1]] = img
    return dst


def letterbox(img: np.ndarray, value: Any):
    """
    Put a pad value on the image to change it to a 1:1 aspect ratio.
    :param img: opencv image
    :param value: pad value(int or tuple)
    :return: opencv image
    """
    channel = 1 if len(img.shape) == 2 else img.shape[2]
    if isinstance(value, int):
        value = tuple([value] * channel)
    N = max(img.shape[:2])
    dst = np.zeros((N, N, img.shape[2]), dtype=np.uint8) + np.array(value, dtype=np.uint8)
    dx = (N - img.shape[1]) // 2
    dy = (N - img.shape[0]) // 2
    dst[dy:dy + img.shape[0], dx:dx + img.shape[1]] = img
    return dst


def _to_image_list(args):
    imgs = []
    for arg in args:
        if isinstance(arg, list):
            imgs += arg
        elif isinstance(arg, np.ndarray):
            imgs.append(arg)
        else:
            pass
    return imgs


def hconcat(*args):
    """
    Return the input images horizontally.
    :param args: opencv image list OR comma seperated images
    :return: opencv image
    """
    imgs = _to_image_list(args)
    max_height = max(img.shape[0] for img in imgs)
    rimgs = [to_color(resize(img, height=max_height)) for img in imgs]
    return cv2.hconcat(rimgs)


def vconcat(*args):
    """
    Return the input images vertically.
    :param args: opencv image list OR comma seperated images
    :return: opencv image
    """
    imgs = _to_image_list(args)
    max_width = max(img.shape[1] for img in imgs)
    rimgs = [to_color(resize(img, width=max_width)) for img in imgs]
    return cv2.vconcat(rimgs)


def canny(img: np.ndarray):
    if len(img.shape) == 3:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    high_th, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    low_th = high_th / 2
    return cv2.Canny(img, low_th, high_th)
