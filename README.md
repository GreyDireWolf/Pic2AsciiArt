# Pic2AsciiArt
A stupid script to convert picture to ascii art (only tested on .png format)
### Installation

Dependency-pillow

Clone the repo,install the pillow via pip and run the script
Usage
```
./main.py <source file> <width> [bg brightness] [bg color] [output file]
Where:
    <source file>: path to your image file
    <width>: desired output picture width: (int) from [2 - +Inf)
    [bg brightness]: bg brightness: (int) from [0; 255]
    [bg color]: bg color: e.g. "black" or "white"
    [output file]: path to output file
```

For example

```sh
python main.py Example/pikachu.png 208 90 black Example/result.png
```
