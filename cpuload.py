#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
from time import sleep
from utils import *
import click
from polyclasses import PolybarInfo

class CPULoad(PolybarInfo):

    """Display the cpu load for polybar."""

    LOAD_CRIT = 30

    def print_condition(self, load):
        return load > self.LOAD_CRIT

    def get_underline_color(self, load):
        prop = prop_between(load, self.LOAD_CRIT, 100)
        return hex_gradient(COLOR_WARM, COLOR_WARN, 1 - prop)

    def format_short(self, load):
        """
        Format the load for polybar.
        """

        return str(round(load)) + '% \uf085'

    def get_args_for_test(self):
        """Generate the args for testing format()."""

        for i in range(0, 101, 5):
            yield i,

    def get_info(self):
        return psutil.cpu_percent(),


if __name__ == "__main__":
    CPULoad().main()
