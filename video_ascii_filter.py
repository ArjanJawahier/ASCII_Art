import cv2
import argparse
from image_ascii_filter import image_to_ascii
import os
import shutil
import glob
from PIL import Image
import pickle
import numpy as np

import time

def video_to_ascii(args, char_brightness):
    # box_size = (args.box_size, args.box_size)

    # tmp_dir = "temp"
    # if os.path.isdir(tmp_dir):
    #     shutil.rmtree(tmp_dir)
    
    # os.mkdir(tmp_dir)

    # vidcap = cv2.VideoCapture(args.video_filename)
    # success, image = vidcap.read()
    # count = 0
    # while success:
    #     # image = image.reshape((image.shape[1], image.shape[0], image.shape[2]))
    #     ascii_image = image_to_ascii(image, box_size, char_brightness, args.color)
    #     framename = f"temp/frame{str(count).zfill(6)}.png"
    #     cv2.imwrite(framename, ascii_image)
    #     print('Created ' + framename)
    #     success, image = vidcap.read()
    #     count += 1

    frames_per_second = 60
    fp_in = "temp/frame*.png"
    fp_out = args.video_filename.split(".")[0] + f"_ascii_{frames_per_second}fps.gif"
    print(fp_out)

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=1000/frames_per_second, loop=0)

    # if os.path.isdir(tmp_dir):
    #     shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert an image into ASCII art.')
    parser.add_argument('video_filename', help="The filename of the video you want to convert.")
    parser.add_argument('box_size', type=int, help="The size of the boxes the ASCII characters will go in.")
    parser.add_argument('--color', action="store_true", help="Whether to use colored ASCII characters.")
    args = parser.parse_args()

    with open("character_brightnesses.data", "rb") as filehandle:
        char_brightness = pickle.load(filehandle)[1:] # Manually removing underscore (_ is bugged -> brightness of 0)

    video_to_ascii(args, char_brightness)

