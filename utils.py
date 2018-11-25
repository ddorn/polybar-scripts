#!/usr/bin/python3

"""
Here are a lot of helper fonctions mostly used for my personal polybar modules.

The color function expect different input:
 - rgb : a red, green, blue tuple of values between 0 and 1
 - RGB : a red, green, blue tuple with integer value between 0 and 255
 - hsv : a hue, saturation, lumiance (or value) tuple of values between 0 and 1
 - hex : a html hexadecimal color of the format #RRGGBB
 - HSV : a hue, saturation, lumiance (or value) tuple. The hue is between 0 and 65535 and th erest is between 0 and 255.

With love by Diego
"""

import os
import colorsys

COLOR_GOOD = os.environ.get('COLOR_GOOD', '#A6E22E')
COLOR_WARM = os.environ.get('COLOR_WARM', '#FFA500')
COLOR_WARN = os.environ.get('COLOR_WARN', '#F92672')
COLOR_DARK = os.environ.get('COLOR_DARK', '#66D9EF')
COLOR_BLACK = os.environ.get('COLOR_BLACK', '#272822')



def rgb_from_hex(h):
    """
    Convert a hexadecimal color to a rgb.
    """

    rgb = h[1:3], h[3:5], h[5:7]
    rgb = list(map(lambda h: int(h, 16)/255, rgb))

    return rgb

def hex_from_rgb(rgb):
    """
    Convert a rgb to a hex color.
    """

    rgb = map(lambda i: hex(int(255 * i))[2:], rgb)
    rgb = map(lambda i: '0' * (2 - len(i)) + i, rgb)
    return '#' + ''.join(rgb)


def rgb_from_RGB(RGB):
    """
    Convert a RGB tuple to a rgb tuple.
    """

    return list(map(lambda i: i / 255, RGB))


def RGB_from_rgb(rgb):
    """
    Convert a rgb tuple to a RGB tuple.
    """

    return list(map(lambda i: int(255 * i), rgb))

def HSV_from_hsv(HSV):
    """
    Convert HSV to hsv.
    """

    return int(65535 * HSV[0]), int(255 * HSV[1]), int(255 * HSV[2])

def hsv_from_HSV(hsv):
    """
    Convert hsv to HSV.
    """

    h, s, l = hsv
    return h / 65535, s / 255, l / 255


hsv_from_rgb = lambda rgb: colorsys.rgb_to_hsv(*rgb)
rgb_from_hsv = lambda hsv: colorsys.hsv_to_rgb(*hsv)

def hsv_gradient(hsv1, hsv2, mix):
    """
    Mix the to hsv color together. return = hsv1 * mix + (1 - mix) * hsv2

    :mix: Coefficient between 0 and 1.
    """

    return list(map(lambda i: mix * i[0] + (1-mix) * i[1], zip(hsv1, hsv2)))

def rgb_gradient(rgb1, rgb2, mix):
    """
    See hsv_gradient.
    """

    return rgb_from_hsv(hsv_gradient(hsv_from_rgb(rgb1), hsv_from_rgb(rgb2), mix))

def RGB_gradient(RGB1, RGB2, mix):
    """
    See hsv_gradient.
    """

    return RGB_from_rgb(rgb_gradient(rgb_from_RGB(RGB1), rgb_from_RGB(RGB2), mix))

def hex_gradient(hex1, hex2, mix):
    """
    See hsv_gradient.
    """

    return hex_from_rgb(rgb_gradient(rgb_from_hex(hex1), rgb_from_hex(hex2), mix))


def underline(text, hex):
    return '%{u' + hex + ' +u}' + text + '%{-u}'

def foreground(text, hex):
    return '%{F' + hex + '}' + text + '%{F}'

def action(text, button, cmd):
    return '%{A' + str(button) + ':' + cmd + ':}' + text + '%{A}'


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def prop_between(value, low=100, high=100):
    """
    Return where value is between low and high, in proportion (useful for gradients).
    The value is clamped between 0 and 1.
    """
    if value <= low:
        return 0
    if value >= high:
        return 1
    return (value - low) / (high - low)
