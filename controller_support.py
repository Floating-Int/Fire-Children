from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Protocol, cast

from displaylib.ascii.prototypes.controller_support import ControllerSupport
from displaylib.math import Vec2

if TYPE_CHECKING:
    from pygame.joystick import JoystickType

class PlayerControllerProtocol(Protocol):
    @property
    def texture(self) -> list[list[str]]: ...
    @texture.setter
    def texture(self, value: list[list[str]]) -> None: ...
    @property
    def treshold(self) -> float: ...
    @treshold.setter
    def treshold(self, value: float) -> None: ...
    @property
    def is_flipped(self) -> bool: ...
    @is_flipped.setter
    def is_flipped(self, value: bool) -> None: ...
    @property
    def direction(self) -> int: ...
    @direction.setter
    def direction(self, value: int) -> None: ...
    @property
    def _update(self) -> function: ...
    @_update.setter
    def _update(self, value: function) -> None: ...
    @property
    def is_moving_left(self) -> bool: ...
    @is_moving_left.setter
    def is_moving_left(self, value: partial) -> None: ...
    @property
    def is_moving_right(self) -> bool: ...
    @is_moving_right.setter
    def is_moving_right(self, value: partial) -> None: ...
    @property
    def is_attacking(self) -> bool: ...
    @is_attacking.setter
    def is_attacking(self, value: partial) -> None: ...
    @property
    def is_shielding(self) -> bool: ...
    @is_shielding.setter
    def is_shielding(self, value: partial) -> None: ...
    @property
    def joystick(self) -> JoystickType: ...
    @joystick.setter
    def joystick(self, value: JoystickType) -> None: ...


RIGHT = 1
LEFT = -1
DIAGONAL_HEIGHT = Vec2(2, 1).normalized().y


def is_moving_left(self) -> bool:
    self = cast(PlayerControllerProtocol, self)
    return self.joystick.get_axis(0) < -self.treshold

def is_moving_right(self) -> bool:
    self = cast(PlayerControllerProtocol, self)
    return self.joystick.get_axis(0) > self.treshold

def is_attacking(self) -> bool:
    self = cast(PlayerControllerProtocol, self)
    if self.joystick.get_button(0):
        return True
    if abs(self.joystick.get_axis(3)) > DIAGONAL_HEIGHT:
        return False
    if (self.joystick.get_button(9) or self.joystick.get_axis(2) < -self.treshold):
        self.texture = [
            [*"   O   "],
            [*"¨¨ | \\ "],
            [*"  / \\  "]
        ]
        self.is_flipped = True
        self.direction = LEFT
        return True
    if self.joystick.get_button(10) or self.joystick.get_axis(2) > self.treshold:
        self.texture = [
            [*"   O   "],
            [*" / | ¨¨"],
            [*"  / \\  "]
        ]
        self.is_flipped = False
        self.direction = RIGHT
        return True
    return False

def is_shielding(self) -> bool:
    self = cast(PlayerControllerProtocol, self)
    if self.joystick.get_button(1):
        return True
    if self.joystick.get_axis(3) > self.treshold and abs(self.joystick.get_axis(3)) >= DIAGONAL_HEIGHT:
        return True
    return False


class CustomControllerSupport(ControllerSupport): # Component (mixin class)
    bindings = [is_moving_left, is_moving_right, is_attacking, is_shielding]
    treshold: float = 0.3

    # def __new__(cls: type[NodeType], *args, device_index: int | None = None, **kwargs) -> NodeType:
    #     if device_index is None:
    #         return super().__new__(cls, *args, **kwargs)
    #     mro_next = cast(MroNext[PlayerControllerProtocol], super())
    #     instance = mro_next.__new__(cls, *args, **kwargs)
    #     try:
    #         instance.joystick = pygame.joystick.Joystick(device_index)
    #     except pygame.error:
    #         return cast(NodeType, instance)
    #     instance._update = _update_wrapper(instance._update)
    #     instance.is_moving_left = partial(is_moving_left, instance)
    #     instance.is_moving_right = partial(is_moving_right, instance)
    #     instance.is_attacking = partial(is_attacking, instance)
    #     instance.is_shielding = partial(is_shielding, instance)
    #     return cast(NodeType, instance)
