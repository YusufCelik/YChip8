from pyglet.graphics import Batch


class CustomBatch(Batch):
    def __init__(self):
        super().__init__()

    def clear_batch(self):
        self.group_map = {}
        self.group_children = {}
        self.top_groups = []
        self._draw_list = []
        self._draw_list_dirty = False