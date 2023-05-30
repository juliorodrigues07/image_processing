from manipulation.punctual_operations import linear_interpolation
from manipulation.punctual_operations import logical_operations
from manipulation.punctual_operations import clumping
from manipulation.punctual_operations import modulus
from manipulation.hist_equalization import equalization
from manipulation.convolution import geometric_filter
from manipulation.convolution import harmonic_filter
from manipulation.convolution import median_filter
from manipulation.convolution import sobel_filter
from manipulation.convolution import alpha_filter
from manipulation.convolution import mean_filter
from manipulation.convolution import min_filter
from manipulation.convolution import max_filter
from manipulation.basic_mods import mirrow_image
from manipulation.basic_mods import show_img
from manipulation.basic_mods import save_img
from os import getcwd
import cv2 as cv


def img_basics():

    img = cv.imread(f'{getcwd()}/images/peppers.tiff')
    mirrow_img = mirrow_image(img)
    save_img(mirrow_img, 'flipped')


def hist_eq():

    # Flag 0 reads only the image's gray channel
    img1 = cv.imread(f'{getcwd()}/images/clock.tiff', 0)
    norm_img = equalization(img1)
    save_img(norm_img, 'normalized_img')


def arithmetics():

    first_img = cv.imread(f'{getcwd()}/images/clock.tiff', 0)
    second_img = cv.imread(f'{getcwd()}/images/airplane.tiff', 0)

    manual = modulus(first_img, second_img, '+')
    # manual = modulus(first_img, second_img, '-')
    # manual = modulus(first_img, second_img, '*')
    # manual = modulus(first_img, second_img, '/')

    # Pretty similar to modulus (except dividing)
    opcv = first_img + second_img
    # opcv = first_img - second_img
    # opcv = first_img * second_img
    # opcv = first_img / second_img

    # Equivalents to clumping
    # opcv = cv.add(first_img, second_img)
    # opcv = cv.subtract(first_img, second_img)
    # opcv = cv.multiply(first_img, second_img)
    # opcv = cv.divide(first_img, second_img)

    show_img(manual, 'Manual')
    show_img(opcv, 'OpenCV')


def logical_stuff():

    first_img = cv.imread(f'{getcwd()}/images/A.png', 0)
    second_img = cv.imread(f'{getcwd()}/images/B.png', 0)

    result = logical_operations(first_img, second_img, '', 'xor', '')
    show_img(result, 'Manual')


def filters():

    img = cv.imread(f'{getcwd()}/images/salt&pepper.png', 0)
    # mean_filter(img)
    # median_filter(img)
    # min_filter(img)
    # max_filter(img)
    # geometric_filter(img)
    # harmonic_filter(img)
    alpha_filter(img)
    # sobel_filter(img)


if __name__ == '__main__':
    # img_basics()
    # hist_eq()
    # arithmetics()
    # logical_stuff()
    filters()
