#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *
import re
from polyclasses import PolybarInfo

class BatteryInfo(PolybarInfo):

    """Display battery info."""

    SHORT_FORMAT_ARGS_NB = 2
    BATTERY_STATUS = ''
    CRITICAL_LEVEL = 20
    FULL_LEVEL = 95

    def get_underline_color(self, battery, *args):
        """
        Get the hexadecimal color corresponding to the given battery.
        """
        battery = prop_between(battery, self.CRITICAL_LEVEL, self.FULL_LEVEL)
        if battery == 0:
            return COLOR_WARN

        return hex_gradient(COLOR_WARN, COLOR_GOOD, 1 - battery)

    def get_info(self):
        """
        Read in the system files to get the battery percentage and wether it's charging.

        :returns: battery, charging
        """

        try:
            with open(r'/sys/class/power_supply/BAT0/capacity') as f:
                battery = int(f.read())
            with open('/sys/class/power_supply/BAT0/status') as f:
                charging = f.read() == 'Charging\n'
        except FileNotFoundError:
            return 0, False

        return battery, charging

    def format_short(self, battery, charging):
        """
        Get the icon in BATTERY_STATUS corresponding to the battery level.
        """

        if charging:
            return self.BATTERY_STATUS[-1]
        if battery <= self.CRITICAL_LEVEL:
            return self.BATTERY_STATUS[0]
        if battery >= self.FULL_LEVEL:
            return self.BATTERY_STATUS[-2]

        v = prop_between(battery, self.CRITICAL_LEVEL, self.FULL_LEVEL)
        v *= len(self.BATTERY_STATUS) - 2
        return self.BATTERY_STATUS[round(v) + 1]

    def format_long(self, battery, charging):
        short = self.format_short(battery, charging)
        short += f' {battery}%'

        return short

    def print_condition(self, battery, *args):
        return battery < self.FULL_LEVEL

    def get_args_for_test(self):
        for i in range(0, 101, 5):
            self.long = i%4 == 0
            yield i, False

        for i in range(0, 101, 20):
            self.long = not self.long
            yield i, True
        self.long = False

if __name__ == "__main__":
    BatteryInfo().main()
