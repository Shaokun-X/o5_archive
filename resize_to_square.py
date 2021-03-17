from skimage.transform import resize
from skimage.io import imread, imsave
import os

for i, file_path in enumerate(os.listdir('image/temp')):
    file_path = os.path.join('image/temp' ,file_path)
    img = imread(file_path)
    new_length = min(img.shape[:2])
    square_img = resize(img, (new_length, new_length))
    imsave(file_path, square_img)
