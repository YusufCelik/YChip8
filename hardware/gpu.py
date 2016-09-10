import pyglet

from emulator import state
from utils.batch import CustomBatch

custom_batch = CustomBatch()


def create_graphics_batch():
    custom_batch.clear_batch()
    display_width = int(640 / 64)
    display_height = int(320 / 32)

    for y_value in range(0, 32):
        for x_value in range(0, 64):
            if state.vram[y_value][x_value] == 1:
                y_cord = 31 - y_value
                custom_batch.add_indexed(4, pyglet.gl.GL_TRIANGLES,
                                         None,
                                         [0, 1, 2, 0, 2, 3],
                                         ('v2i', (
                                             (x_value * display_width),
                                             (y_cord * display_height),
                                             (x_value * display_width) +
                                             display_width,
                                             (y_cord * display_height),
                                             (x_value * display_width) +
                                             display_width,
                                             (y_cord * display_height) +
                                             display_height,
                                             (x_value * display_width),
                                             (y_cord * display_height) +
                                             display_height
                                         )))


def reset():
    custom_batch.clear_batch()
    state.vram = [[0] * 64 for x in range(0, 32)]


def sprite_to_buffer(start_x_pos, start_y_pos, sprite_data, drawing_height):
    x_limit = 8
    outside_screen = False

    if start_y_pos > 31:
        start_y_pos = 0
        outside_screen = True
    elif start_y_pos + drawing_height > 31:
        limit = 32 - start_y_pos
        sprite_data = sprite_data[0:limit]
        drawing_height = limit
        outside_screen = False
    else:
        outside_screen = False

    if start_x_pos > 63:
        start_x_pos = 0
        outside_screen = True
    elif start_x_pos + 8 > 63:
        x_limit = 64 - start_x_pos
        outside_screen = False
    else:
        outside_screen = False

    if outside_screen is False:
        for height in range(0, drawing_height):
            sprite_binary = format(sprite_data[height], '08b')

            for bit in range(0, x_limit):
                if state.vram[start_y_pos + height][start_x_pos + bit] == 1 \
                        and int(sprite_binary[bit]) == 1:
                    state.vx[0xf] = 1
                state.vram[start_y_pos + height][start_x_pos + bit] \
                    ^= int(sprite_binary[bit])
