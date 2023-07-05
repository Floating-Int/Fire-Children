from __future__ import annotations
from displaylib import *
from text_collider import TextCollider


class Shield(TextCollider, Sprite):
    shields: list[Shield] = []
    
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, z_index: int = 0) -> None:
        super().__init__(parent, x=x, y=y, z_index=z_index)
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
        self.health_label = Label(self, text="[===]", x=-2, y=4, color=color.BURLY_WOOD)
        self._health = 15
        self.regen_delay = 1.5
        self.elapsed_time = 0
        self.shields.append(self)
    
    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = value
        self.health_label.text = "[" + (("=" * (value // 5)) + ("-" * int(value % 5 >= 1))).ljust(3) + "]"
    
    def _update(self, _delta: float) -> None:
        if not self.is_deployed and not self.animation.is_playing:
            self.hide()
        else:
            self.show()
    
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
