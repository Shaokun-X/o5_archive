from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import rescale
from skimage.exposure import rescale_intensity
import numpy as np
import multiprocessing


# TRANS_DICT = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# TRANS_DICT = '$B8W#ohbpwZ0LJYzvnrf/|){[?_~>!I:"`.'
# TRANS_DICT = "@&$#%)(*?=!+^`_,-. "
TRANS_DICT = '@%#*+=-:. '


def handle_row(value):
    char_num = len(TRANS_DICT)
    return TRANS_DICT[round(value * (char_num - 1))]


def handle_matrix(row):
    return np.vectorize(handle_row)(row)


def to_ascii(img, rescale_ratio=0):
    """
    Given image should be in gray scale
    Gray pixel value is in [0. 1.0]
    """

    if rescale_ratio != 0 and (isinstance(rescale_ratio, int) or isinstance(rescale_ratio, float)):
        img = rescale(img, rescale_ratio)

    # enhance contrast
    img = rescale_intensity(img, in_range=(img.min(), img.max()))
    
    result = None
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map(handle_matrix, img)
    return result


def write_to_file(result, insert=None):
    """
    @param insert: The charactor to be inserted between each letter in a row.
    """
    if insert is not None and isinstance(insert, str):
        join_base = insert
    else:
        join_base = ''
    with open('ascii_img.txt', 'w', encoding='utf-8') as fp:
        for arr in result:
            fp.write(join_base.join(arr) + '\n')


if __name__ == '__main__':
    # the rgb range is [0,255] for each channel
    py_logo = imread('image/cat.png')

    # the gray range is [0, 1.0]
    gray_py_logo = rgb2gray(py_logo)
    result = to_ascii(gray_py_logo, rescale_ratio=0.01)
    write_to_file(result, insert=' ')  