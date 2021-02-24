"""This file computes the average brightness for each character on the ASCII
table with a decimal value in the range of [33-126]. It does this for the font
UbuntuMono-R.ttf. It then stores the average brightness per character in a 
sorted list of tuples with the format (character, brightness). This list is
stored in a file with the name character_brightnesses.data"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import itertools
import pickle

def average_brightness(img, size):
    arr = np.array(img)
    w, h = size
    total_brightness = 0
    for r, c in itertools.product(range(h), range(w)):
        total_brightness += arr[r, c]
    return total_brightness / (w*h)

def main():
    char_brightness = dict()

    size = (10, 10)
    for i in range(33, 127):
        char = chr(i)
        with Image.new('L', size) as canvas:
            draw = ImageDraw.Draw(canvas)
            monospace_font = ImageFont.truetype("UbuntuMono-R.ttf",10)
            draw.text((0, 0), char, 255, font=monospace_font)
            avg_brightness = average_brightness(canvas, size)
            char_brightness[char] = avg_brightness
            sorted_list = sorted( char_brightness.items(), key=lambda x:x[1])

    with open("character_brightnesses.data", "wb") as filehandle:
        pickle.dump(sorted_list, filehandle)
    
if __name__ == "__main__":
    main()