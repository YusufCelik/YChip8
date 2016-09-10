import pyglet
from pyglet.gl import *

from hardware import keyboard, ram, gpu
from emulator import state, instructions
from utils import debug


class Chip8(pyglet.window.Window):
    batch = pyglet.graphics.Batch()

    def __init__(self, rom_file):
        super(Chip8, self).__init__(
            fullscreen=False,
            caption='Chip8 Emulator',
            width=640,
            height=320,
            vsync=False)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.fps = pyglet.clock.ClockDisplay()
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        ram.load_fonts()
        self.load_rom('roms/%s' % rom_file)

    def on_draw(self):
        self.clear()
        gpu.custom_batch.draw()
        self.fps.draw()

    def on_key_release(self, symbol, modifiers):
        keyboard.set_key(symbol)

    def load_rom(self, rom_path):
        binary = open(rom_path, 'rb').read()
        i = 0
        while i < len(binary):
            state.memory[i + 0x200] = binary[i]
            i += 1

    def update(self, dt):
        instruction = (
            state.memory[state.program_counter:(state.program_counter + 2)])
        combined_instruction = ''.join('{:02x}'.format(x) for x in instruction)
        debug.debug_log(combined_instruction)

        instructions.executeOpcode(int(combined_instruction, 16))

        if state.delay_timer > 0:
            state.delay_timer -= 1

        if state.sound_timer > 0:
            state.sound_timer -= 1
