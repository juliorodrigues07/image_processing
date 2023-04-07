from numpy import zeros
from numpy import uint8
from numpy import max
from numpy import min
import cv2 as cv


def preprocessing(first_image, second_image):

    # For images which differs in height and/or width shapes (might need some tweaks in some methods to run)
    # height = min([first_image.shape[0], second_image.shape[0]])
    # width = min([first_image.shape[1], second_image.shape[1]])

    height = first_image.shape[0]
    width = first_image.shape[1]

    # Resizes the image, providing equal shapes for operations (both will have the same height and width in pixels)
    if second_image.shape[0] != height or second_image.shape[1] != width:
        second_image = cv.resize(src=second_image.copy(), dsize=(width, height), interpolation=cv.INTER_CUBIC)

    return height, width, second_image


def clumping(first_image, second_image, operator):

    pixels = list()
    height, width, second_image = preprocessing(first_image, second_image.copy())

    for h in range(height):

        aux = list()
        for w in range(width):

            first_operand = int(first_image[h][w])
            second_operand = int(second_image[h][w])

            # Always truncates the result if the value surpasses the upper bound (255)
            if operator == '+':
                if first_operand + second_operand > 255:
                    aux.append(255)
                else:
                    aux.append(first_operand + second_operand)

            # Always truncates the result if the value is lower than the lower bound (0)
            elif operator == '-':
                if first_operand - second_operand < 0:
                    aux.append(0)
                else:
                    aux.append(first_operand - second_operand)

            elif operator == '*':
                if first_operand * second_operand > 255:
                    aux.append(255)
                else:
                    aux.append(first_operand * second_operand)

            elif operator == '/':
                aux.append(int(first_operand / second_operand) if second_operand > 0 else first_operand)

        pixels.append(aux)
        del aux

    new_img = zeros((height, width, 1), dtype=uint8)
    cv.rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)

    for h in range(height):
        for w in range(width):
            new_img[h][w] = pixels[h][w]

    return new_img


def modulus(first_image, second_image, operator):

    pixels = list()
    height, width, second_image = preprocessing(first_image, second_image.copy())

    for h in range(height):

        aux = list()
        for w in range(width):

            first_operand = int(first_image[h][w])
            second_operand = int(second_image[h][w])

            if operator == '+':
                if first_operand + second_operand > 255:
                    aux.append((first_operand + second_operand) % 255)
                else:
                    aux.append(first_operand + second_operand)

            elif operator == '-':
                if first_operand - second_operand < 0:
                    aux.append((first_operand - second_operand) % 255)
                else:
                    aux.append(first_operand - second_operand)

            elif operator == '*':
                if first_operand * second_operand > 255:
                    aux.append((first_operand * second_operand) % 255)
                else:
                    aux.append(first_operand * second_operand)

            elif operator == '/':
                aux.append(int(first_operand * 255 / second_operand) % 255 if second_operand > 0 else first_operand)

        pixels.append(aux)
        del aux

    new_img = zeros((height, width, 1), dtype=uint8)
    cv.rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)

    for h in range(height):
        for w in range(width):
            new_img[h][w] = pixels[h][w]

    return new_img


def linear_interpolation(first_image, second_image, operator):

    pixels = list()
    height, width, second_image = preprocessing(first_image, second_image.copy())

    for h in range(height):

        aux = list()
        for w in range(width):

            first_operand = int(first_image[h][w])
            second_operand = int(second_image[h][w])

            if operator == '+':
                aux.append(first_operand + second_operand)
            elif operator == '-':
                aux.append(first_operand - second_operand)
            elif operator == '*':
                aux.append(first_operand * second_operand)
            elif operator == '/':
                aux.append(int(first_operand / second_operand) if second_operand > 0 else second_operand)

        pixels.append(aux)
        del aux

    # Old pixels' range
    old_min_value = min(pixels)
    old_max_value = max(pixels)
    old_range = old_max_value - old_min_value

    # New pixels' range
    new_min_value = 0
    new_max_value = 255
    new_range = new_max_value - new_min_value

    new_img = zeros((height, width, 1), dtype=uint8)
    cv.rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)
    
    for h in range(height):
        for w in range(width):

            # Linear interpolation to map new range (0 up to 255)
            old_pixel = pixels[h][w]
            new_pixel = int(((old_pixel - old_min_value) / old_range) * new_range + new_min_value)
            new_img[h][w] = new_pixel

    return new_img


def logical_operations(first_image, second_image, unary_op1, bin_op, unary_op2):

    height, width, second_image = preprocessing(first_image, second_image.copy())

    # Binarizes both images --> Tone < 128 = 0 (Black) | Tone >= 128 = 255 (White)
    for h in range(first_image.shape[0]):
        for w in range(first_image.shape[1]):
            if first_image[h][w] < 128:
                first_image[h][w] = 0
            else:
                first_image[h][w] = 255

    for h in range(second_image.shape[0]):
        for w in range(second_image.shape[1]):
            if second_image[h][w] < 128:
                second_image[h][w] = 0
            else:
                second_image[h][w] = 255

    # _, binary_img = cv.threshold(first_image, 128, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # test = cv.bitwise_xor(first_image, second_image)
    # cv.imshow('test', test)
    # cv.waitKey(0)

    new_img = zeros((height, width, 1), dtype=uint8)
    cv.rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)

    # TODO: Simplify and optimize from here onwards
    # Interpret 255 as False and 0 as True
    for h in range(height):
        for w in range(width):

            # NOT(IMG 1) {AND, OR, XOR} NOT(IMG 2)
            if unary_op1 == 'not' and unary_op2 == 'not':
                if bin_op == 'and':
                    new_img[h][w] = 0 if first_image[h][w] == 255 and second_image[h][w] == 255 else 255
                elif bin_op == 'or':
                    new_img[h][w] = 0 if first_image[h][w] == 255 or second_image[h][w] == 255 else 255
                elif bin_op == 'xor':
                    new_img[h][w] = 0 if (first_image[h][w] == 255 and second_image[h][w] == 0)\
                                      or (first_image[h][w] == 0 and second_image[h][w] == 255) else 255

            # NOT(IMG 1) {AND, OR, XOR} IMG 2
            elif unary_op1 == 'not' and unary_op2 == '':
                if bin_op == 'and':
                    new_img[h][w] = 0 if first_image[h][w] == 255 and second_image[h][w] == 0 else 255
                elif bin_op == 'or':
                    new_img[h][w] = 0 if first_image[h][w] == 255 or second_image[h][w] == 0 else 255
                elif bin_op == 'xor':
                    new_img[h][w] = 0 if (first_image[h][w] == 255 and second_image[h][w] == 0)\
                                      or (first_image[h][w] == 0 and second_image[h][w] == 255) else 255

            # IMG 1 {AND, OR, XOR} NOT(IMG 2)
            elif unary_op1 == '' and unary_op2 == 'not':
                if bin_op == 'and':
                    new_img[h][w] = 0 if first_image[h][w] == 0 and second_image[h][w] == 255 else 255
                elif bin_op == 'or':
                    new_img[h][w] = 0 if first_image[h][w] == 0 or second_image[h][w] == 255 else 255
                elif bin_op == 'xor':
                    new_img[h][w] = 0 if (first_image[h][w] == 0 and second_image[h][w] == 255)\
                                      or (first_image[h][w] == 255 and second_image[h][w] == 0) else 255

            # IMG 1 {AND, OR, XOR} IMG 2
            else:
                if bin_op == 'and':
                    new_img[h][w] = 0 if first_image[h][w] == 0 and second_image[h][w] == 0 else 255
                elif bin_op == 'or':
                    new_img[h][w] = 0 if first_image[h][w] == 0 or second_image[h][w] == 0 else 255
                elif bin_op == 'xor':
                    new_img[h][w] = 0 if (first_image[h][w] == 0 and second_image[h][w] == 255)\
                                      or (first_image[h][w] == 255 and second_image[h][w] == 0) else 255

    return new_img
