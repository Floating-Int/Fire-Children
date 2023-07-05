from displaylib import *


class Ground(Sprite):
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.texture = [
            list("¨" * 64)
        ]
        self.color = color.SEA_GREEN
