from manipulation.punctual_operations import linear_interpolation
from manipulation.punctual_operations import clumping
from manipulation.punctual_operations import modulus
from manipulation.hist_equalization import equalization
from manipulation.basic_mods import mirrow_image
from manipulation.basic_mods import show_img
from manipulation.basic_mods import save_img
from os import getcwd
import cv2 as cv


def main():

    # img = imread(getcwd() + '/images/peppers.tiff')
    # mirrow_img = mirrow_image(img)
    # save_img(mirrow_img, 'flipped')

    # Flag 0 reads only the image's gray channel
    # img1 = imread(f'{getcwd()}/images/clock.tiff', 0)
    # norm_img = equalization(img1)
    # save_img(norm_img, 'normalized_img')

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


if __name__ == '__main__':
    main()
