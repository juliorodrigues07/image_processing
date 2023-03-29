from os.path import isdir
from os import getcwd
from os import chdir
from os import mkdir
import cv2 as cv


chdir('..')
if not isdir(f'{getcwd()}/exports'):
    mkdir(f'{getcwd()}/exports')    


def show_img(img, title='my_picture'):

    cv.imshow(title, img)
    cv.waitKey(0)


def save_img(img, title='my_picture'):

    cv.imwrite(f'{getcwd()}/exports/{title}.tiff', img)


def split_channels(img):

    b, g, r = cv.split(img)

    show_img(b, 'blue')
    show_img(g, 'green')
    show_img(r, 'red')

    return r, g, b


def merge_channels(r, g, b):

    merged = cv.merge((b, g, r))
    show_img(merged, 'merged')


def fill_color(img):

    img[40:90, 120:380] = (0, 0, 0)
    show_img(img)


def mirrow_image(img):

    show_img(img, 'before')

    height = img.shape[0]
    width = img.shape[1]
    mirrow_img = img.copy()

    for x in range(height): 
        for y in range(width):
            mirrow_img[x][y] = img[x][img.shape[1] - 1 - y]

    show_img(mirrow_img, 'flipped')
    return mirrow_img
