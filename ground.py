from displaylib import * # type: ignore


class Ground(Sprite):
    color = color.SEA_GREEN
    
    def __init__(self, parent: AnyNode | None = None, x: float = 0, y: float = 0, z_index: int = 0, force_sort: bool = True) -> None:
        self.texture = [
            list("¨" * 64)
        ]
