from emulator import state, instructions


class TestChip8:
    def test_6xkk(self):
        instructions.x6XKK(0x6018)

        assert state.vx[0] == 24

    def test_7xkk(self):
        state.vx[1] = 1
        instructions.x7XKK(0x71ff)

        assert state.vx[1] == (1 + 0xff) & 255

    def test_8xy0(self):
        state.vx[0] = 0
        state.vx[1] = 5
        instructions.x8XY0(0x8010)

        assert state.vx[0] == 5

