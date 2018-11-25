#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
import sys
import hue


def get_light_text(light_id):
    """
    Get the text to outpt for a given light.
    """

    l = hue.Light(light_id, True)
    if l.on:
        color = list(l.hsl)
        color[1] = 200
        color[2] = 255
        color = hex_from_rgb(rgb_from_hsv(hsv_from_HSV(color)))
        light = ' \uf834 '
    else:
        color = '#555555'
        light = ' \uf400 '

    # add forground color
    light = foreground(light, color)
    # add underline
    light = underline(light, color)
    # Add actions on click
    cmd = f'hue.py put {light_id} --toggle'
    light = action(light, 1, cmd)

    return light


def main():
    s = ' '.join(get_light_text(i) for i in range(1, 3))
    print(s)

if __name__ == "__main__":
    main()
