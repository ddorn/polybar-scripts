#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from utils import *
from psutil import virtual_memory

TOTAL_RAM = 16 * 2**30
RAM_CRIT = 3 * 2**30

def format(ram):
    if ram < RAM_CRIT:
        return ""

    s = bytes2human(ram)
    s = ' ' + s
    s = underline(s, hex_gradient(COLOR_WARM, COLOR_WARN, 1 - (ram / TOTAL_RAM)))

    return s

def test_format(ctx, param, value):
    if not value:
        return

    for i in range(0, TOTAL_RAM, 1*2**30):
        print(format(i), end=' ')
    print()

@click.command()
@click.option('--test', is_flag=1, callback=test_format, expose_value=False)
def main():
    v = virtual_memory()
    t = v.used + v.shared
    print(format(t))


if __name__ == "__main__":
    main()
