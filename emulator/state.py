memory = [0] * 4096
vx = [0] * 16
key_pressed_index = None
vram = [[0] * 64 for x in range(0, 32)]
program_counter = 0x200
delay_timer = 0
stack = [0] * 16
stack_pointer = 0
register_index = 0
sound_timer = 0
debug = False
