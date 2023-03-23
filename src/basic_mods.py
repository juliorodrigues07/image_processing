import cv2 as cv
from os import getcwd
from os import chdir


def show_img(img, title='my_picture'):

    cv.imshow(title, img)
    cv.waitKey(0)


def save_img(img, title='my_picture'):

    cv.imwrite(f'{getcwd()}/images/{title}.tiff', img)


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
    # save_img(mirrow_img, 'flipped')


def main():

    chdir('..')
    img = cv.imread(getcwd() + '/images/peppers.tiff')
    
    # show_img(img)
    # r, g, b = split_channels(img)
    # merge_channels(r, g, b)
    # fill_color(img)
    
    mirrow_image(img)


if __name__ == '__main__':
    main()
