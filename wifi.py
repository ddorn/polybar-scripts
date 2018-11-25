#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from utils import *
import re
import click
import subprocess
import signal

WIFI_SYMBOL = ''
WIFI_CRITICAL = 50
LONG = False


def toggle_long(*args):
    global LONG
    LONG = not LONG
    print_wifi()


signal.signal(signal.SIGUSR1, toggle_long)


def format(wifi, name='', long=False):
    """
    Format the wifi for polybar.

    wifi: Signal strength between 0 and 1
    name: wifi name
    long: show the name or not
    """

    if not wifi or not name or 'off/any' in name:
        return ''


    wifi = int(wifi * 100)
    if wifi < WIFI_CRITICAL:
        color = COLOR_WARN
    else:
        color = hex_gradient(COLOR_GOOD, COLOR_WARM, (wifi - WIFI_CRITICAL) / (100 - WIFI_CRITICAL))

    text = WIFI_SYMBOL
    if long:
        name = name.strip(' "')
        text += f' {wifi}% at {name}'
    text = underline(text, color)

    return text


def test_format(ctx, param, value):
    if not value:
        return

    for i in range(0, 101, 10):
        print(format(i/100, str(i), i%3), end=' ')

    print()


def get_wifi():
    """
    Get the wifi status based on iwconfig.
    """

    out = subprocess.check_output('iwconfig wlp2s0'.split()).decode()

    match = re.search('ESSID:(.*)$', out, re.M)
    name = 'off/any' if not match else match.group(1)

    match = re.search(r'Link Quality=(\d+)/(\d+) .*', out)
    strength = o if not match else int(match.group(1)) / int(match.group(2))

    return strength, name


def print_wifi():
    print(format(*get_wifi(), LONG), flush=True)


@click.command()
@click.option('--test', is_flag=1, callback=test_format, expose_value=False)
@click.option('--interval', '-i', default=1.0, help='Time between updates')
def main(interval):
    """
    Output wifi status for polybar.
    """

    while True:
        print_wifi()
        sleep(interval)

if __name__ == "__main__":
    main()
