#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from itertools import imap
__title__ = u'Pic2AsciiArt'
__version__=0.1

FONT = u"fonts/FSEX300.ttf"
FONTSIZE = 15
CELLWIDTH = 10
CELLHEIGHT = 14
BRIGHTNESS = 80


import sys
import os
import time

from PIL import (
    Image, ImageFont, ImageDraw, ImageFilter
)

import charset


def timer (f):
    def w (*a, **kw):
        s = time.time()
        r = f(*a, **kw)
        #print u"{}{} ++> {:g} secs.".format(f.__name__, a, time.time() - s)
        return r
    return w


def usage ():
    message = (
        u'=======================================================================\n'
        u'{app} version {ver}\n\n'
        u'Usage:\n'
        u'{0} <source file> <width> [bg brightness] [bg color] [output file]\n\n'
        u'Where:\n'
        u'\t<source file>: path to your image file\n'
        u'\t<width>: desired output picture width: (int) from [2 - +Inf)\n'
        u'\t[bg brightness]: bg brightness: (int) from [0; 255]\n'
        u'\t[bg color]: bg color: e.g. "black" or "white"\n'
        u'\t[output file]: path to output file\n\n'
        # TODO: font
        # TODO: fontsize
        u'======================================================================='
    ).format(sys.argv[0], ver=__version__, app=__title__)
    print >>sys.stderr, unicode(message)
    sys.exit(1)


def spinCursor ():
    cursor = '-\|/'
    i = 0
    while True:
        yield cursor[i]
        i = (i + 1) % cursor.__len__()


def bgColor (source, w, h, br):
    for i in xrange(0, w):
        for j in xrange(0, h):
            yield tuple(imap((lambda x: abs(x-br) if x > br else 0), list(source.getpixel((i, j)))))


def fontColor (source, w, h):
    for i in xrange(0, w):
        for j in xrange(0, h):
            pxColor = source.getpixel((i, j))
            yield (pxColor, (reduce(lambda x, y: x+y, pxColor) // 3 * (charset.total - 1)) // 255)


@timer
def main ():
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
            backgroundColor = u"black"
        try:
            outputFilePath = sys.argv[5]
        except:
            outputFilePath = sourceImagePath + u".(ASCII).png"

    try:
        sourceImage = Image.open(sourceImagePath)
        print "Loaded image with size:", sourceImage.size
    except:
        print >>sys.stderr, u"An error has occured while opening image..."
        exit(1)

    outputHeight = (outputWidth * sourceImage.size[1]) // sourceImage.size[0]

    background = Image.new(u"RGBA", (outputWidth, outputHeight), u"white")
    sourceImage = sourceImage.filter(ImageFilter.SHARPEN).resize((outputWidth, outputHeight), Image.ANTIALIAS)
    sourceImage = Image.alpha_composite(background, sourceImage).convert(u"RGB")

    # sourceImage.show()
    print u"Output image size in chars: ({w}, {h})".format(w=outputWidth, h=outputHeight)

    font = ImageFont.truetype(FONT, FONTSIZE)
    wStep = CELLWIDTH
    hStep = CELLHEIGHT
    fntClrGen = fontColor(sourceImage, outputWidth, outputHeight)
    bgClrGen = bgColor(sourceImage, outputWidth, outputHeight, brightness)
    outputWidth *= wStep
    outputHeight *= hStep

    outputImage = Image.new(u"RGB", (outputWidth, outputHeight), backgroundColor)
    print u"Output image size: ({w}, {h})".format(w=outputWidth, h=outputHeight)

    draw = ImageDraw.Draw(outputImage)
    print u"Using charset with {} chars total".format(charset.total)
    print u"File will be saved to: {x}".format(x=os.getcwdu()), u"\nProcessing..."

    # spinner = spinCursor()
    for i in xrange(0, outputWidth, wStep):
        for j in xrange(0, outputHeight, hStep):
            # print(spinner.__next__(), end='\b')
            draw.rectangle([i, j, i+wStep, j+hStep], u"rgb{}".format(bgClrGen.next()))
            charClr = fntClrGen.next()
            draw.text((i+1, j-1), charset.chars[int(charClr[1])], fill=u"rgb{}".format(charClr[0]), font=font)

    # print('\b', end='\b')

    outputImage.save(outputFilePath, u"PNG")
    print u"Converted & saved successfully to: {o}".format(o=outputFilePath)


if __name__ == u'__main__':
    main()
