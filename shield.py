from displaylib import *
from text_collider import TextCollider


class Shield(TextCollider, Sprite):
    shields = []
    
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0) -> None:
        super().__init__(parent, x=x, y=y)
        self.texture = [
            [" "],
            [" "],
            [" "]
        ]
        self.color = color.BURLY_WOOD
        self.is_deployed = False
        self.animation = AnimationPlayer(
            self,
            Spawn=Animation("./animations/shield"),
            Despawn=Animation("./animations/shield", reverse=True)
        )
        self.shields.append(self)
    
    def activate(self) -> None:
        if self.is_deployed:
            return
        self.animation.play("Spawn")
        self.is_deployed = True

    def deactivate(self) -> None:
        if not self.is_deployed:
            return
        self.animation.play("Despawn")
        self.is_deployed = False
    
    def queue_free(self) -> None:
        if self in self.shields:
            self.shields.remove(self)
        super().queue_free()
