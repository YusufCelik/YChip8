from random import randint

from emulator import state
from hardware import gpu, keyboard


def executeOpcode(opcode):
    """
    Function mapped to a specific opcode or opcode family will
     be executed.
    :param opcode:
    """
    if (opcode & 0xf0ff) == 0x00e0 or (opcode & 0xf0ff) == 0x00ee:
        instruction = opcode & 0xf0ff
    elif (opcode & 0xf000) == 0xf000:
        if (opcode & 0xf00f) == 0xf007 or (opcode & 0xf00f) == 0xf00a:
            instruction = opcode & 0xf00f
        else:
            instruction = opcode & 0xf0ff
    elif (opcode & 0xf000) == 0x8000:
        instruction = opcode & 0xf00f
    elif (opcode & 0xf0ff) == 0xe0a1 or (opcode & 0xf0ff) == 0xe09e:
        instruction = opcode & 0xf0ff
    else:
        instruction = opcode & 0xF000

    funcs[instruction](opcode)


def Zero(opcode):
    """
    Regular 0 opcodes were machine code, and
    will therefore be ignored
    """
    state.program_counter += 2


def x00E0(opcode):
    """Clear the screen"""
    gpu.reset()
    state.program_counter += 2


def x00EE(opcode):
    """
    Return from a subroutine.
    The interpreter sets the program counter to the address
    at the top of the state.stack,
    then subtracts 1 from the state.stack pointer.
    """
    state.program_counter = state.stack[-1]
    state.stack.pop()
    state.program_counter += 2


def x1NNN(opcode):
    """Jump to address NNN"""
    state.program_counter = (opcode & 0x0FFF)


def x2NNN(opcode):
    """Execute subroutine starting at address NNN"""
    state.stack.append(state.program_counter)
    state.program_counter = (opcode & 0x0FFF)


def x3XKK(opcode):
    """Skip the following instruction if the value of register VX equals NN"""
    vx_index = (opcode & 0x0F00) >> 8
    cmp_value = (opcode & 0x00ff)

    if state.vx[vx_index] == cmp_value:
        state.program_counter += 4
    else:
        state.program_counter += 2


def x4XKK(opcode):
    """
    Skip the following instruction if the value of register VX
    is not equal to NN
    """
    vx_index = (opcode & 0x0F00) >> 8
    cmp_value = (opcode & 0x00ff)

    if state.vx[vx_index] != cmp_value:
        state.program_counter += 4
    else:
        state.program_counter += 2


def x5XY0(opcode):
    """
    Skip the following instruction if the value of register VX
    is equal to the value of register VY
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    if state.vx[vx_index] == state.vx[vy_index]:
        state.program_counter += 4
    else:
        state.program_counter += 2


def x6XKK(opcode):
    """Store number NN in register VX"""
    vx_index = (opcode & 0x0F00) >> 8
    vx_value = (opcode & 0x00FF)

    state.vx[vx_index] = vx_value
    state.program_counter += 2


def x7XKK(opcode):
    """Add the value NN to register VX"""
    vx_index = (opcode & 0x0F00) >> 8
    vx_new_value = (opcode & 0x00FF)

    vx_result = state.vx[vx_index] + vx_new_value
    vx_result &= 255

    state.vx[vx_index] = vx_result
    state.program_counter += 2


def x8XY0(opcode):
    """Store the value of register VY in register VX"""
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] = state.vx[vy_index]
    state.program_counter += 2


def x8XY1(opcode):
    """Set VX to VX OR VY"""
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] |= state.vx[vy_index]
    state.program_counter += 2


def x8XY2(opcode):
    """Set VX to VX AND VY"""
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4
    state.vx[vx_index] &= state.vx[vy_index]
    state.program_counter += 2


def x8XY3(opcode):
    """Set VX to VX XOR VY"""
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] ^= state.vx[vy_index]
    state.program_counter += 2


def x8XY4(opcode):
    """
    Add the value of register VY to register VX
    Set VF to 01 if a carry occurs
    Set VF to 00 if a carry does not occur
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] += state.vx[vy_index]

    if state.vx[vx_index] > 255:
        state.vx[0xf] = 1
        state.vx[vx_index] &= 255
    else:
        state.vx[0xf] = 0

    state.program_counter += 2


def x8XY5(opcode):
    """
    Subtract the value of register VY from register VX
    Set VF to 00 if a borrow occurs
    Set VF to 01 if a borrow does not occur
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] -= state.vx[vy_index]

    if state.vx[vx_index] < 0:
        state.vx[0xf] = 0
        state.vx[vx_index] &= 255
    else:
        state.vx[0xf] = 1

    state.program_counter += 2


def x8XY6(opcode):
    """
    Store the value of register VY shifted right one bit in register VX
    Set register VF to the least significant bit prior to the shift
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    binary_string = bin(state.vx[vy_index])
    if binary_string[len(binary_string) - 1] == '1':
        state.vx[0xf] = 1
    elif binary_string[len(binary_string) - 1] == '0':
        state.vx[0xf] = 0

    state.vx[vy_index] = state.vx[vy_index] >> 1
    state.vx[vx_index] = state.vx[vy_index]
    state.program_counter += 2


def x8XY7(opcode):
    """
    Set register VX to the value of VY minus VX
    Set VF to 00 if a borrow occurs
    Set VF to 01 if a borrow does not occur
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    state.vx[vx_index] = state.vx[vy_index] - state.vx[vx_index]

    if state.vx[vx_index] < 0:
        state.vx[0xf] = 1
        state.vx[vx_index] = 0
    else:
        state.vx[0xf] = 0

    state.program_counter += 2


def x8XYE(opcode):
    """
    Store the value of register VY shifted left one bit in register VX
    Set register VrF to the most significant bit prior to the shift
    """
    vx_index = (opcode & 0x0f00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    binary_string = bin(state.vx[vy_index])
    if binary_string[len(binary_string) - 1] == '1':
        state.vx[0xf] = 1
    elif binary_string[len(binary_string) - 1] == '0':
        state.vx[0xf] = 0

    state.vx[vy_index] = state.vx[vy_index] << 1
    state.vx[vx_index] = state.vx[vy_index]
    state.program_counter += 2


def x9XY0(opcode):
    """
    Skip the following instruction if the value of register VX
    is not equal to the value of register VY
    """
    vx_index = (opcode & 0x0F00) >> 8
    vy_index = (opcode & 0x00f0) >> 4

    if state.vx[vx_index] != state.vx[vy_index]:
        state.program_counter += 4
    else:
        state.program_counter += 2


def ANNN(opcode):
    """Store memory address NNN in register I"""
    i_value = (opcode & 0x0FFF)
    state.register_index = i_value
    state.program_counter += 2


def BNNN(opcode):
    """Jump to address NNN + V0"""
    state.program_counter = (opcode & 0x0FFF) + state.vx[0]


def CXKK(opcode):
    """Set VX to a random number with a mask of NN"""
    vx_index = (opcode & 0x0F00) >> 8
    kk_value = (opcode & 0x00FF)
    rnd_value = randint(0, 255)
    toset_value = rnd_value & kk_value
    state.vx[vx_index] = toset_value
    state.program_counter += 2


def DXYN(opcode):
    """
    DRWDraw a sprite at position VX, VY with N bytes
    of sprite data starting at the address stored in I
    Set VF to 01 if any set pixels are changed to unset, and 00 otherwise
    """
    drawing_height = (opcode & 0x000F)
    start_x_cord = state.vx[(opcode & 0x0F00) >> 8]
    start_y_cord = state.vx[(opcode & 0x00f0) >> 4]

    endoffset = state.register_index + drawing_height
    draw_data = state.memory[state.register_index:endoffset]

    state.vx[0xf] = 0

    gpu.sprite_to_buffer(start_x_cord, start_y_cord, draw_data, drawing_height)
    gpu.create_graphics_batch()

    state.program_counter += 2


def EX9E(opcode):
    """
    Skip the following instruction if the key corresponding
    to the hex value currently stored in register VX is pressed
    """
    vx_index = (opcode & 0x0f00) >> 8

    if state.key_pressed_index == state.vx[vx_index]:
        state.program_counter += 4
        keyboard.reset()
    else:
        state.program_counter += 2


def EXA1(opcode):
    """
    Skip the following instruction if the key corresponding to the hex
    value currently stored in register VX is not pressed
    """
    vx_index = (opcode & 0x0f00) >> 8

    if state.key_pressed_index != state.vx[vx_index]:
        state.program_counter += 4
    else:
        keyboard.reset()
        state.program_counter += 2


def FX07(opcode):
    """Store the current value of the delay timer in register VX"""
    vx_index = (opcode & 0x0F00) >> 8
    state.vx[vx_index] = state.delay_timer
    state.program_counter += 2


def FX0A(opcode):
    """Wait for a keypress and store the result in register VX"""
    vx_index = (opcode & 0x0f00) >> 8

    if state.key_pressed_index is not None:
        state.vx[vx_index] = state.key_pressed_index
        keyboard.reset()
        state.program_counter += 2


def FX15(opcode):
    """ Set the delay timer to the value of register VX"""
    vx_index = (opcode & 0x0F00) >> 8
    state.delay_timer = state.vx[vx_index]
    state.program_counter += 2


def FX18(opcode):
    """Set the sound timer to the value of register VX"""
    vx_index = (opcode & 0x0f00) >> 8
    state.sound_timer = state.vx[vx_index]
    state.program_counter += 2


def FX1E(opcode):
    """Add the value stored in register VX to register I"""
    vx_index = (opcode & 0x0F00) >> 8
    state.register_index += state.vx[vx_index]
    state.program_counter += 2


def FX29(opcode):
    """Set I to the memory address of the sprite data corresponding
    to the hexadecimal digit stored in register VX"""
    vx_index = (opcode & 0x0F00) >> 8
    state.register_index = state.vx[vx_index] * 0x5

    state.program_counter += 2


def FX33(opcode):
    """
    Store the binary-coded decimal equivalent
    of the value stored in register VX at addresses I, I+1, and I+2
    """
    vx_index = (opcode & 0x0F00) >> 8
    bcd_value = '{:03d}'.format(state.vx[vx_index])
    state.memory[state.register_index] = int(bcd_value[0])
    state.memory[state.register_index + 1] = int(bcd_value[1])
    state.memory[state.register_index + 2] = int(bcd_value[2])
    state.program_counter += 2


def FX55(opcode):
    """Store the values of registers V0 to VX inclusive
    in memory starting at address I.
    I is set to I + X + 1 after operation
    """
    last_index = (opcode & 0x0F00) >> 8

    if last_index > 0:
        for index in range(0, last_index + 1):
            state.memory[state.register_index + index] = state.vx[index]
    else:
        state.memory[state.register_index] = state.vx[last_index]

    state.program_counter += 2


def FX65(opcode):
    """Fill registers V0 to VX inclusive with the values stored in
    memory starting at address I.
    I is set to I + X + 1 after operation
    """
    last_index = (opcode & 0x0F00) >> 8

    if last_index > 0:
        for index in range(0, last_index + 1):
            state.vx[index] = state.memory[state.register_index + index]
    else:
        state.vx[last_index] = state.memory[state.register_index]

    state.program_counter += 2


funcs = {
    0x0000: Zero,
    0x00ee: x00EE,
    0x00e0: x00E0,
    0x1000: x1NNN,
    0x2000: x2NNN,
    0x3000: x3XKK,
    0x4000: x4XKK,
    0x5000: x5XY0,
    0x6000: x6XKK,
    0x7000: x7XKK,
    0x8000: x8XY0,
    0x8001: x8XY1,
    0x8002: x8XY2,
    0x8003: x8XY3,
    0x8004: x8XY4,
    0x8005: x8XY5,
    0x8006: x8XY6,
    0x8007: x8XY7,
    0x800e: x8XYE,
    0x9000: x9XY0,
    0xa000: ANNN,
    0xb000: BNNN,
    0xc000: CXKK,
    0xd000: DXYN,
    0xe0a1: EXA1,
    0xe09e: EX9E,
    0xf007: FX07,
    0xf00a: FX0A,
    0xf015: FX15,
    0xf018: FX18,
    0xf01e: FX1E,
    0xf029: FX29,
    0xf033: FX33,
    0xf055: FX55,
    0xf065: FX65
}
