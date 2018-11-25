#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psutil import cpu_percent
from time import sleep
from utils import *
import click

LOAD_CRIT = 30

def format(load):
    """
    Format the load for polybar.
    """

    if load < LOAD_CRIT:
        return ""

    color = hex_gradient(COLOR_WARM, COLOR_WARN, 1 -  (load - LOAD_CRIT) / (100 - LOAD_CRIT))


    load = str(round(load)) + '% \uf085'
    load = underline(load, color)

    return load

def test_format(ctx, param, value):
    if not value:
        return

    for i in range(0, 101, 5):
        print(format(i), end='', flush=False)
    print(flush=1)
    sleep(10)

@click.command()
@click.option('--test', is_flag=1, callback=test_format, expose_value=False)
def main():
    """
    Give anice cpu load
    """

    while 1:
        load = cpu_percent()
        print(format(load), flush=True)
        sleep(1)


if __name__ == "__main__":
    main()
