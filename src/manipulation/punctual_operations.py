from numpy import zeros
from numpy import uint8
from numpy import max
from numpy import min
from cv2 import rectangle
from cv2 import resize
from cv2 import INTER_CUBIC


def preprocessing(first_image, second_image):

    # For images which differs in height and/or width shapes
    # height = min([first_image.shape[0], second_image.shape[0]])
    # width = min([first_image.shape[1], second_image.shape[1]])

    height = first_image.shape[0]
    width = first_image.shape[1]

    # Resizes the image, providing equal shapes for operations (both will have the same height and width in pixels)
    if second_image.shape[0] != height or second_image.shape[1] != width:
        second_image = resize(src=second_image.copy(), dsize=(width, height), interpolation=INTER_CUBIC)

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

    # Creates a blank image, based on the shape of the image past for operation
    new_img = zeros((height, width, 1), dtype=uint8)
    rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)

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

            # TODO: logics
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

    # Creates a blank image, based on the shape of the image past for operation
    new_img = zeros((height, width, 1), dtype=uint8)
    rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)

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

            # TODO: logics
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

    # Creates a blank image, based on the shape of the image past for operation
    new_img = zeros((height, width, 1), dtype=uint8)
    rectangle(new_img, (0, 0), (width, height), (255, 255, 255), -1)
    
    for h in range(height):
        for w in range(width):

            # Linear interpolation to map new range (0 up to 255)
            old_pixel = pixels[h][w]
            new_pixel = int(((old_pixel - old_min_value) / old_range) * new_range + new_min_value)
            new_img[h][w] = new_pixel

    return new_img
