from emulator import state
from prettytable import PrettyTable


def debug_log(combined_instruction):
    v_labels = [str('V%s' % hex(x)) for x in range(0, 16)]
    v_data = [hex(state.vx[x]) for x in range(0, 16)]
    debug_labels = ['instruction',
                    'program_counter',
                    'register_index',
                    *v_labels]
    debug_data = ['inst 0x%s' % combined_instruction,
                  hex(state.program_counter),
                  hex(state.register_index), *v_data]
    table = PrettyTable()
    table.field_names = debug_labels
    table.add_row(debug_data)
    if state.debug is True:
        print(table)
