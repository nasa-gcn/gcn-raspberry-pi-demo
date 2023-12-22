#!/usr/bin/env python
import functools
import shlex
import signal
import subprocess
import sys

import gpiozero
import typer


def call(command):
    print(command, file=sys.stderr)
    subprocess.call(shlex.split(command))


def main(command_1: str, command_2: str):
    commands = [command_1, command_2]
    buttons = [gpiozero.Button(i) for i in [23, 24]]
    for button, command in zip(buttons, commands):
        button.when_activated = functools.partial(call, command)
    signal.pause()


if __name__ == "__main__":
    typer.run(main)
