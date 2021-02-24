from PIL import Image, ImageDraw, ImageFont
import argparse
import pickle
import numpy as np
from itertools import product
from ascii_brightness import average_brightness

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

def main():
    parser = argparse.ArgumentParser(description='Convert an image into ASCII art.')
    parser.add_argument('image_filename', help="The filename of the image you want to convert.")
    parser.add_argument('box_size', type=int, help="The size of the boxes the ASCII characters will go in.")
    args = parser.parse_args()

    with open("character_brightnesses.data", "rb") as filehandle:
        char_brightness = pickle.load(filehandle)[1:] # Manually removing underscore (_ is bugged -> brightness of 0)
        max_char_brightness = char_brightness[-1][1]

    box_size = (args.box_size, args.box_size)
    
    with Image.open(args.image_filename).convert('L') as original_img:
        original_imgarr = np.array(original_img)
        shape = original_imgarr.shape
        num_vertical = shape[0]//box_size[0]
        num_horizontal = shape[1]//box_size[1]
        avg_brightness = np.zeros((num_vertical, num_horizontal))
        for row_block, col_block in product(range(num_vertical), range(num_horizontal)):
            r, c = row_block * box_size[0], col_block * box_size[1]
            avg_brightness[row_block, col_block] = average_brightness(
                original_imgarr[r:r+box_size[0], c:c+box_size[1]], 
                box_size
            ) / (255 / max_char_brightness)

    with Image.new('L', original_img.size) as ascii_img:
        draw = ImageDraw.Draw(ascii_img)
        monospace_font = ImageFont.truetype("UbuntuMono-R.ttf", args.box_size+2)
        for row_block, col_block in product(range(num_vertical), range(num_horizontal)):
            char = find_best_fitting_char(avg_brightness, char_brightness, row_block, col_block)
            if char:
                draw.text((col_block*box_size[1], row_block*box_size[0]), char, 255, font=monospace_font)

        new_img_filename = args.image_filename.split(".")[0] + f"_ascii_{args.box_size}.jpg"
        ascii_img.save(new_img_filename, "JPEG")

if __name__ == "__main__":
    main()