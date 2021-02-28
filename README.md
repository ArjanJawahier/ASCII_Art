# Image to ASCII converter

This program converts any picture into ASCII art. Currently only works if the font UbuntuMono-R is installed (it is by default in Ubuntu).
Install dependencies using the command `pip3 install -r requirements.txt`.
Run with the command `python3 image_ascii_filter.py <img_file> <char_size> [--color]`. If `--color` is specified, the ASCII characters are written in the average color of the neighbourhood of that ASCII character.

## Examples:
![scene12_original](images/scene12.png?raw=true)
![scene12_ascii5](images/scene12_ascii_5.jpg?raw=true)
![scene12_ascii10](images/scene12_ascii_10_color.jpg?raw=true)
![scene12_ascii15](images/scene12_ascii_15.jpg?raw=true)

Manually compressed example GIF (the original GIF was 103 MB):

![GIF_plons](images/sample7_ascii_compressed.gif?raw=true)