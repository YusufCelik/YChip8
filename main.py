import argparse

import pyglet

from emulator.chip8 import Chip8

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", help="Select game rom by title")
    args = parser.parse_args()
    chip8 = Chip8(args.rom)
    pyglet.clock.schedule_interval(chip8.update, 1 / 360)
    pyglet.app.run()