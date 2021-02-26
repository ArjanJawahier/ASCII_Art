from PIL import Image, ImageDraw, ImageFont
import argparse
import pickle
import numpy as np
from itertools import product
from ascii_brightness import average_brightness
from color_functions import *

def find_best_fitting_char(avg_brights, char_brights, row_block, col_block):
    """
    This function computes the best fitting character to be put in
    the block [row_block, col_block] in the new ASCII image.
    The chosen character will have a similar (relative) brightness level
    as the block of pixels in the original image.
    """
    value = avg_brights[row_block, col_block]
    for char, bright in char_brights[::-1]:
        if bright <= value:
            return char
    return char


def average_hsv(img, size, max_char_brightness):
    arr = np.array(img)
    w, h = size
    total_color = np.zeros(3)
    for r, c in product(range(h), range(w)):
        total_color += arr[r, c]
    average_color = total_color / (w*h)

    avg_hsv = rgb_to_hsv(average_color)
    if np.any(np.isnan(avg_hsv)):
        avg_hsv = np.zeros(3)
    else:
        scaling_factor = max_char_brightness / 255
        avg_hsv[2] *= scaling_factor

    return avg_hsv


def conversion(use_color):
    if use_color:
        return 'RGB'
    else:
        return 'L'

def compute_filling_color(avg_hsv, row_block, col_block):
    hsv = avg_hsv[row_block, col_block]
    hsv[2] = 1.0
    rgb = hsv_to_rgb(hsv) * 255
    rgba_tuple = (int(rgb[0]), int(rgb[1]), int(rgb[2]), 255)
    return rgba_tuple


def main():
    parser = argparse.ArgumentParser(description='Convert an image into ASCII art.')
    parser.add_argument('image_filename', help="The filename of the image you want to convert.")
    parser.add_argument('box_size', type=int, help="The size of the boxes the ASCII characters will go in.")
    parser.add_argument('--color', action="store_true", help="Whether to use colored ASCII characters.")
    args = parser.parse_args()

    box_size = (args.box_size, args.box_size)

    with open("character_brightnesses.data", "rb") as filehandle:
        char_brightness = pickle.load(filehandle)[1:] # Manually removing underscore (_ is bugged -> brightness of 0)
        max_char_brightness = char_brightness[-1][1]

        
    with Image.open(args.image_filename).convert(conversion(args.color)) as original_img:
        original_imgarr = np.array(original_img)
        shape = original_imgarr.shape
        num_vertical = shape[0]//box_size[0]
        num_horizontal = shape[1]//box_size[1]
        avg_hsv = np.zeros((num_vertical, num_horizontal, 3))

        for row_block, col_block in product(range(num_vertical), range(num_horizontal)):
            r, c = row_block * box_size[0], col_block * box_size[1]
            block = original_imgarr[r:r+box_size[0], c:c+box_size[1]]
            avg_hsv[row_block, col_block] = average_hsv(block, box_size, max_char_brightness)


    with Image.new(conversion(args.color), original_img.size) as ascii_img:
        draw = ImageDraw.Draw(ascii_img)
        monospace_font = ImageFont.truetype("UbuntuMono-R.ttf", args.box_size+2)
        for row_block, col_block in product(range(num_vertical), range(num_horizontal)):
            char = find_best_fitting_char(avg_hsv[:, :, 2], char_brightness, row_block, col_block)
            if char:
                if args.color:
                    fill = compute_filling_color(avg_hsv, row_block, col_block)
                else:
                    fill = 255
                draw.text((col_block*box_size[1], row_block*box_size[0]), char, fill=fill, font=monospace_font)


        if args.color:
            new_img_filename = args.image_filename.split(".")[0] + f"_ascii_{args.box_size}_color.jpg"
        else:
            new_img_filename = args.image_filename.split(".")[0] + f"_ascii_{args.box_size}.jpg"
        ascii_img.save(new_img_filename, "JPEG")

if __name__ == "__main__":
    main()