import matplotlib.pyplot as plt
import seaborn as sns


def plot_dist(i, j, show_x, title):
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.histplot(x=i, y=j, palette='Purples')

    ax.set(xlabel=None)
    ax.set_title(title)
    ax.set_ylabel("Amount", fontsize=18)
    ax.set_xlabel("Ton", fontsize=18)

    if not show_x:
        plt.tick_params(labelbottom=False)
    plt.show()

    # fig.savefig()


def equalization(img):

    probs, cumulative, normalized, pixels_normalized = list(), list(), list(), list()
    pixels = [0] * 256
    tones = [i for i in range(256)]
    eight_scale = [f'{i} / 7' for i in range(8)]
    gray_lvls = [i / 7 for i in range(8)]

    # Counts tone frequency based on each image pixel
    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            idx = img[h][w]
            pixels[idx] += 1

    # plot_dist(tones, pixels, False, 'Pixels Distribution (0 to 255)')

    # Pixels quantity
    tally = sum(pixels)
    for i in range(len(gray_lvls)):

        # Multiply by 255 to obtain the tone integer value
        upper_bound = round(gray_lvls[i] * 255)
        split = 0
        
        if i > 0:
            lower_bound = round(gray_lvls[i - 1] * 255)

            # Uses tone value as an index on pixels' list, to map each ton probability (8 scale)
            split = sum(pixels[lower_bound : upper_bound])
        else:
            split = sum(pixels[0 : upper_bound])

        pixels_normalized.append(split)
        probs.append(split / tally)
        cumulative.append(sum(probs))

    for value in cumulative:
        for i in range(len(gray_lvls)):
            
            # Maps the new gray tone between gray levels range interval, according to cumulative probabilities
            if i > 0:
                if value > gray_lvls[i - 1] and value < gray_lvls[i]:
                    normalized.append(gray_lvls[i - 1])
                elif value == gray_lvls[i]:
                    normalized.append(gray_lvls[i])
            else:
                if value > gray_lvls[i] and value < gray_lvls[i + 1]:
                    normalized.append(gray_lvls[i])
                    break
                elif value == gray_lvls[i + 1]:
                    normalized.append(gray_lvls[i + 1])

    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            idx = img[h][w] / 255

            # Applies the new gray tone to the pixels
            for i in range(len(normalized)):
                if i > 0:
                    if idx > normalized[i - 1] and idx <= normalized[i]:
                        img[h][w] = round(normalized[i - 1] * 255)
                else:
                    if idx > normalized[i] and idx <= normalized[i + 1]:
                        img[h][w] = round(normalized[i] * 255)

    print('NORMALIZATION\n')
    print(f'Before: {list(map(lambda x: int(x * 7), gray_lvls))}')
    print(f'After: {list(map(lambda x: int(x * 7), normalized))}')

    # plot_dist(eight_scale, pixels_normalized, True, 'Pixels Distribution (0 to 7)')
    return img
