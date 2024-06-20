from __future__ import annotations
import random
import math
from displaylib import * # type: ignore


class FireParticle(Sprite):
    FORWARD = 1
    BACKFORWARD = -1
    _SPEED = 5
    _ANGLE_VARIATION = 2 # from negative to positive
    _ANGLE_DIVIDER = 10.0
    _INCREASE = 2
    _FLIGHT_VARIATION = 1.2
    _MIN_LIFETIME = 5
    _MAX_LIFETIME = 20
    _LIFETIME_DIVIDER = 10
    _COLORS = [
        color.rgb_color(200+idx*2, 90+idx*8) for idx in range(20)
    ]
    texture = [["#"]]
    particles: list[FireParticle] = []

    def __init__(self, parent: AnyNode | None = None, x: float = 0, y: float = 0, force_sort: bool = True, direction: int = FORWARD, speed_modifier: float = 1.0) -> None:
        self.direction = direction
        self._speed_modifier = speed_modifier
        self.color = random.choice(self._COLORS)
        num = random.randint(0, 5)
        if num > 4:
            self.texture = [["."]]
        elif num > 2:
            self.texture = [["*"]]
        self._start_position = Vec2(x, y)
        self._angle = random.randint(-self._ANGLE_VARIATION, self._ANGLE_VARIATION) / self._ANGLE_DIVIDER
        self._elapsed_time = 0.0
        self._lifetime = random.randint(self._MIN_LIFETIME, self._MAX_LIFETIME) / self._LIFETIME_DIVIDER / speed_modifier
        if random.randint(0, 2) == 0:
            self.position.y -= 1
        self.particles.append(self)
    
    def _update(self, delta: float) -> None:
        self._elapsed_time += delta
        if self._elapsed_time >= self._lifetime:
            self.queue_free()
        self.position.x = self._start_position.x + math.floor(self._elapsed_time * self._speed_modifier * self._SPEED) * self.direction
        self.position.y = self._start_position.y + math.floor(self._movement_fn(self._elapsed_time * self._speed_modifier * self._SPEED)) * self.direction
        if (self.position.y - self._start_position.y) > 3 or (self.position.y - self._start_position.y) < -3:
            self.queue_free()
    
    def _movement_fn(self, x: float) -> float:
        return self._angle * (self._INCREASE * x + x** self._FLIGHT_VARIATION * math.sin(x))

    def queue_free(self) -> None:
        if self in self.particles:
            self.particles.remove(self)
        super().queue_free()
