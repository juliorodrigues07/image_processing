from manipulation.punctual_operations import linear_interpolation
from manipulation.hist_equalization import equalization
from manipulation.basic_mods import mirrow_image
from manipulation.basic_mods import show_img
from manipulation.basic_mods import save_img
from cv2 import imread
from os import getcwd


def main():

    # img = imread(getcwd() + '/images/peppers.tiff')
    # mirrow_img = mirrow_image(img)
    # save_img(mirrow_img, 'flipped')

    # Flag 0 reads only the image's gray channel
    # img1 = imread(f'{getcwd()}/images/clock.tiff', 0)
    # norm_img = equalization(img1)
    # save_img(norm_img, 'normalized_img')

    img1 = imread(f'{getcwd()}/images/clock.tiff', 0)
    img2 = imread(f'{getcwd()}/images/airplane.tiff', 0)

    added1 = linear_interpolation(img1, img2, '+')
    added2 = img1 + img2
    show_img(added1, 'sum1')
    show_img(added2, 'sum2')


if __name__ == '__main__':
    main()
