#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2013 tuurngait <tuurngait@icloud.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""


__title__ = 'pic2ascii'
__version__ = '0.2'
__author__ = 'tuurngait'
__license__ = 'Do What The Fuck You Want To Public License'
__copyright__ = '(c) 2013, tuurngait <tuurngait@icloud.com>'


FONT = "fonts/FSEX300.ttf"
FONTSIZE = 15
CELLWIDTH = 10
CELLHEIGHT = 14
BRIGHTNESS = 80


import sys
import os
import time

from functools import reduce

from PIL import (
    Image, ImageFont, ImageDraw, ImageFilter
)

import charset


def timer (f: callable) -> callable:
    def w (*a: list, **kw: dict) -> object:
        s = time.time()
        r = f(*a, **kw)
        print("{}{} ++> {:g} secs.".format(f.__name__, a, time.time() - s))
        return r
    return w


def usage () -> None:
    message = (
        '=======================================================================\n'
        '{app} version {ver}\n\n'
        'Usage:\n'
        '{0} <source file> <width> [bg brightness] [bg color] [output file]\n\n'
        'Where:\n'
        '\t<source file>: path to your image file\n'
        '\t<width>: desired output picture width: (int) from [2 - +Inf)\n'
        '\t[bg brightness]: bg brightness: (int) from [0; 255]\n'
        '\t[bg color]: bg color: e.g. "black" or "white"\n'
        '\t[output file]: path to output file\n\n'
        # TODO: font
        # TODO: fontsize
        '======================================================================='
    ).format(sys.argv[0], ver=__version__, app=__title__)
    print(str(message), file=sys.stderr)
    sys.exit(1)


def spinCursor () -> str:
    cursor = r'-\|/'
    i = 0
    while True:
        yield cursor[i]
        i = (i + 1) % cursor.__len__()


def bgColor (source: Image, w: int, h: int, br: int) -> (int, int, int):
    for i in range(0, w):
        for j in range(0, h):
            yield tuple(map((lambda x: abs(x-br) if x > br else 0), list(source.getpixel((i, j)))))


def fontColor (source: Image, w: int, h: int) -> ((int, int, int), int):
    for i in range(0, w):
        for j in range(0, h):
            pxColor = source.getpixel((i, j))
            yield (pxColor, (reduce(lambda x, y: x+y, pxColor) // 3 * (charset.total - 1)) // 255)


@timer
def main () -> None:
    # TODO: use optparse or argparse or optparse or smth else
    if len(sys.argv) < 2:
        usage()
    else:
        sourceImagePath = sys.argv[1]
        outputWidth = int(sys.argv[2]) if int(sys.argv[2]) > 1 else usage()
        try:
            brightness = 255 - int(sys.argv[3]) if int(sys.argv[3]) < 256 else 0
        except:
            brightness = BRIGHTNESS
        try:
            backgroundColor = sys.argv[4]
        except:
            backgroundColor = "black"
        try:
            outputFilePath = sys.argv[5]
        except:
            outputFilePath = sourceImagePath + ".(ASCII).png"

    try:
        sourceImage = Image.open(sourceImagePath)
        print("Loaded image with size:", sourceImage.size)
    except:
        print("An error has occured while opening image...", file=sys.stderr)
        exit(1)

    outputHeight = (outputWidth * sourceImage.size[1]) // sourceImage.size[0]

    background = Image.new("RGBA", (outputWidth, outputHeight), "white")
    sourceImage = sourceImage.filter(ImageFilter.SHARPEN).resize((outputWidth, outputHeight), Image.ANTIALIAS)
    sourceImage = Image.alpha_composite(background, sourceImage).convert("RGB")

    # sourceImage.show()
    print("Output image size in chars: ({w}, {h})".format(w=outputWidth, h=outputHeight))

    font = ImageFont.truetype(FONT, FONTSIZE)
    wStep = CELLWIDTH
    hStep = CELLHEIGHT
    fntClrGen = fontColor(sourceImage, outputWidth, outputHeight)
    bgClrGen = bgColor(sourceImage, outputWidth, outputHeight, brightness)
    outputWidth *= wStep
    outputHeight *= hStep

    outputImage = Image.new("RGB", (outputWidth, outputHeight), backgroundColor)
    print("Output image size: ({w}, {h})".format(w=outputWidth, h=outputHeight))

    draw = ImageDraw.Draw(outputImage)
    print("Using charset with {} chars total".format(charset.total))
    print("File will be saved to: {x}".format(x=os.getcwd()), "\nProcessing...")

    # spinner = spinCursor()
    for i in range(0, outputWidth, wStep):
        for j in range(0, outputHeight, hStep):
            # print(spinner.__next__(), end='\b')
            draw.rectangle([i, j, i+wStep, j+hStep], "rgb{}".format(bgClrGen.__next__()))
            charClr = fntClrGen.__next__()
            draw.text((i+1, j-1), charset.chars[int(charClr[1])], fill="rgb{}".format(charClr[0]), font=font)

    # print('\b', end='\b')

    outputImage.save(outputFilePath, "PNG")
    print("Converted & saved successfully to: {o}".format(o=outputFilePath))


if __name__ == '__main__':
    main()
