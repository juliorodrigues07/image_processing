import numpy as np
import cv2 as cv


# Image operations mask
mask = np.ones((3, 5), dtype=np.float64)
mask_height = mask.shape[0]
mask_width = mask.shape[1]
height_bound = int(mask_height / 2)
width_bound = int(mask_width / 2)


def show_mods(before, after, operation):

    cv.imshow('Before', before)
    cv.imshow(f'{operation} Filter', after)

    while True:
        key = cv.waitKey(0) & 0xFF
        if key == 27:
            break

    cv.destroyAllWindows()


def apply_filter(h, w, img):

    total = list()

    for s in range(int(-mask_height / 2), int(mask_height / 2) + 1):
        for t in range(int(-mask_width / 2), int(mask_width / 2) + 1):
            total.append((mask[s + 1][t + 1]) * img[h + s][w + t])

    return total


def mean_filter(img):

    operation = 'Mean'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            total = apply_filter(h, w, img)
            mod_img[h][w] = sum(total) / (mask_height * mask_width)
            # mod_img[h][w] = np.mean(total)

    show_mods(img, mod_img, operation)


def median_filter(img):

    operation = 'Median'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            total = apply_filter(h, w, img)
            total.sort()
            mod_img[h][w] = total[len(total) // 2]

    show_mods(img, mod_img, operation)


def min_filter(img):

    operation = 'Min'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            total = apply_filter(h, w, img)
            mod_img[h][w] = min(total)

    show_mods(img, mod_img, operation)


def max_filter(img):

    operation = 'Max'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            total = apply_filter(h, w, img)
            mod_img[h][w] = max(total)

    show_mods(img, mod_img, operation)


def geometric_filter(img):

    operation = 'Geometric'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            # Removing zeros
            total = apply_filter(h, w, img)
            new_total = [i for i in total if i != 0]

            # Multiply all pixels' values and calculates n-th square root from the result
            pixel = pow(np.prod(new_total), 1 / len(new_total))
            mod_img[h][w] = pixel

    show_mods(img, mod_img, operation)


def harmonic_filter(img):

    operation = 'Harmonic'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            check = False
            total = apply_filter(h, w, img)

            # If one of the values is zero, the harmonic mean is zero
            for i in range(len(total)):
                if total[i] != 0:
                    total[i] = 1 / total[i]
                else:
                    check = True
                    break

            pixel = 0 if check else (mask_height * mask_width) / sum(total)
            mod_img[h][w] = pixel

    show_mods(img, mod_img, operation)


def alpha_filter(img):

    operation = 'Alpha'
    d = 4
    discard = int(d / 2)
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    if d >= (mask_height * mask_width):
        print('d must be smaller than the total of elements in the mask')
        exit(0)

    for h in range(height_bound, height - height_bound):
        for w in range(width_bound, width - width_bound):

            total = apply_filter(h, w, img)
            total.sort()

            # Removes d/2 elements from the start and end of the ascending sorted list
            for i in range(discard):
                total.pop(0)
                total.pop()

            mod_img[h][w] = np.mean(total)

    show_mods(img, mod_img, operation)


def sobel_filter(img):

    operation = 'Sobel'
    height = img.shape[0]
    width = img.shape[1]
    mod_img = img.copy()

    gx = np.array([[1.0, 0.0, -1.0], [2.0, 0.0, -2.0], [1.0, 0.0, -1.0]])
    gy = np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])

    for h in range(1, height - 1):
        for w in range(1, width - 1):

            # Gx * A | Gy * A
            r1 = np.multiply(gx, img[h - 1: h + 2, w - 1: w + 2])
            r2 = np.multiply(gy, img[h - 1: h + 2, w - 1: w + 2])

            # √ (Gx ^ 2 + Gy ^ 2)
            pixel = np.sqrt(pow(np.sum(r1), 2) + pow(np.sum(r2), 2))
            mod_img[h][w] = pixel

    show_mods(img, mod_img, operation)
