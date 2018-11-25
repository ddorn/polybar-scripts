#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from utils import *
import click
import subprocess
import signal


class PolybarInfo:
    """
    Base class to show info in polybar.

    This class is not meant to be instancited more than once.
    """

    SHORT_FORMAT_ARGS_NB = 1

    def __init__(self):
        signal.signal(signal.SIGUSR1, self.toggle_long)
        self.long = False

    def toggle_long(self, *args):
        self.long = not self.long
        self.print_info()

    def format(self, *args):
        """
        Format the info for polybar.

        info: args for format_short this is the first return value from get_info()
        extra: args for format_short this is the rest of the values from get_info()
        long: show the extra or not
        """

        if not self.print_condition(*args):
            return ""

        if self.long:
            text = self.format_long(*args)
        else:
            text = self.format_short(*args[:self.SHORT_FORMAT_ARGS_NB])

        text = " " + text + " "
        text = underline(text, self.get_underline_color(*args))
        text = action(text, 1, f'kill -USR1 {os.getpid()} -USR1')

        return text

    def print_info(self):
        print(self.format(*self.get_info()), flush=True)

    def main(self):

        @click.command()
        @click.option('--test', is_flag=1, callback=self.test_format, expose_value=False)
        @click.option('--interval', '-i', default=1.0, help='Time between updates')
        def main(interval):
            """
            Output info status for polybar.
            """

            while True:
                self.print_info()
                sleep(interval)

        main()

    def test_format(self, ctx, param, value):
        if not value:
            return

        for i in self.get_args_for_test():
            print(self.format(*i), end=' ', flush=False)

        print(flush=True)
        sleep(10)

    # To Override

    def print_condition(self, *args):
        """
        Return True if we need to print the info.
        False disables printing.
        """
        raise NotImplementedError

    def get_underline_color(self, *args):
        """Return the underline hex color for the given value."""
        raise NotImplementedError

    def get_info(self):
        """
        Get the info status.
        """

        info = 14, 'coucou', ...

        raise NotImplementedError


    def get_args_for_test(self):
        """
        This should yield fake args to test the format function.
        It must yield same args (type and number) as get_info().
        """
        raise NotImplementedError

    def format_long(self, *args):
        raise NotImplementedError

    def format_short(self, *args):
        raise NotImplementedError


if __name__ == "__main__":
    help(PolybarInfo)
