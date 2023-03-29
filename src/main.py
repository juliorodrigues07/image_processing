from manipulation.gray_equalization import equalization
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
    img = imread(getcwd() + '/images/clock.tiff', 0)
    norm_img = equalization(img)
    # save_img(norm_img, 'normalized_img')


if __name__ == '__main__':
    main()
