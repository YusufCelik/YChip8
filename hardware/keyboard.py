from pyglet.window import key

from emulator import state

keymap = {
    key.Q: 0x1,
    key.W: 0x2,
    key.E: 0x3,
    key.A: 0x4,
    key.S: 0x5,
    key.D: 0x6,
    key.Z: 0x7,
    key.X: 0x8,
    key.C: 0x9,
    key.R: 0xa,
    key.F: 0xb,
    key.V: 0xc,
    key.T: 0xd,
    key.G: 0xe,
    key.B: 0xf,
    key.SPACE: 0x0
}


def set_key(key_value):
    state.key_pressed_index = keymap.get(key_value)


def reset():
    state.key_pressed_index = None
