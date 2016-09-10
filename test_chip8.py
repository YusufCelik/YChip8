from emulator.chip8 import Chip8

class TestChip8:

    def test_1nnn(self):
        chip8 = Chip8()
        chip8.x1NNN(0x1123)
        assert chip8.program_counter == 0x123

    def test_annn(self):
        chip8 = Chip8()
        chip8.register_index = 0
        chip8.ANNN(0xa123)
        assert chip8.register_index == 0x123

    def test_fx1e(self):
        chip8 = Chip8()
        chip8.register_index = 10
        chip8.vx = [44, 12, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        chip8.FX1E(0xf11e)
        assert chip8.register_index == 22

    def test_fx29(self):
        chip8 = Chip8()
        chip8.register_index = 0
        chip8.vx = [44, 1, 23, 58, 41, 52, 61, 7, 80, 9, 10, 11, 12, 13, 14, 15]
        chip8.FX29(0xf029)
        assert chip8.register_index == 44

    # The interpreter copies the values of registers V0 through Vx into memory,
    # starting at the address in I.
    def test_fx55(self):
        chip8 = Chip8()
        chip8.register_index = 2
        chip8.vx = [44, 1, 23, 58, 41]
        chip8.memory = [2, 4, 5, 6, 8, 10]
        chip8.FX55(0xf255)
        assert chip8.memory[2:5] == chip8.vx[0:3]

    def test_fx65(self):
        chip8 = Chip8()
        chip8.memory = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        chip8.vx = [0, 0, 0, 0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        chip8.FX65(0xf465)
        assert chip8.vx == chip8.memory

    def test_3xkk(self):
        chip8 = Chip8()
        chip8.vx = [16]
        chip8.program_counter = 0
        chip8.x3XKK(0x3010)
        assert chip8.program_counter == 4

    def test_4xkk(self):
        chip8 = Chip8()
        chip8.vx = [16]
        chip8.program_counter = 0
        chip8.x4XKK(0x4000)
        assert chip8.program_counter == 4

    def test_5xkk(self):
        chip8 = Chip8()
        chip8.vx = [16, 16]
        chip8.program_counter = 0
        chip8.x5XY0(0x5010)
        assert chip8.program_counter == 4

    def test_6xkk(self):
        chip8 = Chip8()
        chip8.vx = [44, 1, 23, 58, 41, 52, 61, 7, 80, 9, 10, 11, 12, 13, 14, 15]
        chip8.x6XKK(0x6010)
        assert chip8.vx[0] == 0x10

    def test_7xkk(self):
        chip8 = Chip8()
        chip8.vx = [44, 1, 23, 58, 41, 52, 61, 7, 80, 9, 10, 11, 12, 13, 14, 15]
        chip8.x7XKK(0x7005)
        assert chip8.vx[0] == 49




