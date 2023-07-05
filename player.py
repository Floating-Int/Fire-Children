import enum
import random
from displaylib import *
import keyboard
from shield import Shield
from fire import FireParticle
from text_collider import TextCollider


RIGHT = 1
LEFT = -1

class State(enum.IntEnum):
    IDLE = 1
    WALKING = 2
    SHIELDING = 3
    ATTACKING = 4


class PlayerTemplate(TextCollider, Sprite):
    frame: int = 0
    state: State = State.IDLE

    def __new__(cls, *args, label_position=None, skin=None, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, label_position: Vec2 = Vec2(0, 0), skin=color.STEEL_BLUE) -> None:
        super().__init__(parent, x=x, y=y)
        self.texture = [
            [*"   O   "],
            [*" / | \\ "],
            [*"  / \\  "]
        ]
        self.color = skin
        self._health = 10
        self._fuel = 20
        self._fuel_cooldown = 1.7 # seconds
        self.direction = RIGHT
        self.is_flipped = False
        self.has_flipped = False
        self.anim_player = AnimationPlayer(
            self,
            WalkRight=Animation("./animations/walk"),
            WalkLeft=Animation("./animations/walk", fliph=True)
        )
        self.shield = Shield(z_index=3)
        self.shield.set_global_position(self.get_global_position() + Vec2(9, 0))
        self.health_label = Label(text="[=====]", x=label_position.x, y=label_position.y, color=color.CRIMSON)
        self.fire_label = Label(text="[=====]", x=label_position.x, y=label_position.y+1, color=color.DARK_CYAN)
        self._fuel_elapsed_time = 0
    
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value: int) -> None:
        self._health = value
        if value <= 0:
            self.health_label.text = f"[     ]"
            return
        self.health_label.text = "[" + (("=" * (value // 2)) + ("-" * (value % 2))).ljust(5) + "]"

    @property
    def fuel(self) -> int:
        return self._fuel

    @fuel.setter
    def fuel(self, value: int) -> None:
        self._fuel = value
        self.fire_label.text = "[" + (("=" * (value // 4)) + ("-" * int(value % 4 >= 1))).ljust(5) + "]"

    def is_moving_left(self) -> bool:
        return False
    
    def is_moving_right(self) -> bool:
        return False
    
    def is_attacking(self) -> bool:
        return False
    
    def is_shielding(self) -> bool:
        return False

    def _update(self, delta: float) -> bool:
        if self.state == State.IDLE:
            walked = False
            velocity = Vec2()
            if not (self.is_moving_left() and self.is_moving_right()):
                if self.is_moving_left():
                    velocity.x -= 1
                    self.direction = LEFT
                    self.is_flipped = True
                    self.state = State.WALKING
                    walked = True
                elif self.is_moving_right():
                    velocity.x += 1
                    self.direction = RIGHT
                    self.is_flipped = False
                    self.state = State.WALKING
                    walked = True
                self.move_and_slide(velocity)
            # regen fuel
            self._fuel_elapsed_time += delta
            if self.fuel < 20 and self._fuel_elapsed_time >= self._fuel_cooldown:
                self.fuel += 1
            # -- after movement
            if not walked and self.is_shielding(): # arrow down
                self.state = State.SHIELDING
                self.anim_player.stop()
            elif not walked and self.is_attacking(): # arrow up
                self._fuel_elapsed_time = 0
                self.state = State.ATTACKING
                self.anim_player.stop()
                self.texture = [
                    [*"   O   "],
                    [*" / | ¨¨"],
                    [*"  / \\  "]
                ]
            elif walked:
                if not self.anim_player.is_playing:
                    if self.direction == RIGHT:
                        self.anim_player.play("WalkRight")
                    else:
                        self.anim_player.play("WalkLeft")
                else:
                    if self.direction == RIGHT:
                        if not self.anim_player.current_animation == "WalkRight":
                            self.anim_player.play("WalkRight")
                    else:
                        if not self.anim_player.current_animation == "WalkLeft":
                            self.anim_player.play("WalkLeft")
            elif not self.anim_player.is_playing:
                self.texture = [
                    [*"   O  "],
                    [*" / | \\"],
                    [*"  / \\ "]
                ]

        if self.state == State.WALKING:
            self.state = State.IDLE
            self.texture = [
                [*"   O   "],
                [*" / | \\ "],
                [*"  / \\  "]
            ]

        if self.state == State.ATTACKING:
            # stop fuel regen
            self._fuel_elapsed_time = 0
            if self.frame != 1:
                match self.frame:
                    case 0:
                        self.texture = [
                            [*"   O   "],
                            [*" / | ¨¨"],
                            [*"  / \\  "]
                        ]
                        if self.is_flipped:
                            self.texture = text.mapfliph(self.texture)
                self.frame += 1
            elif not self.is_attacking():
                self.state = State.IDLE
                self.frame = 0
                self.has_flipped = False
            else:
                a = self.is_moving_left()
                b = self.is_moving_right()
                if not self.has_flipped and ((a and not b) or (not a and b)): # nand + xor
                    if a:
                        if not self.direction == LEFT:
                            self.texture = text.mapfliph(self.texture)
                            self.direction = LEFT
                            self.has_flipped = True
                            self.is_flipped = not self.is_flipped
                    else:
                        if not self.direction == RIGHT:
                            self.texture = text.mapfliph(self.texture)
                            self.direction = RIGHT
                            self.has_flipped = True
                            self.is_flipped = not self.is_flipped

                if self.fuel > 0:
                    self.fuel -= 1
                    if self.direction == LEFT:
                        particle = FireParticle(x=self.position.x-1, y=self.position.y+1, direction=self.direction, speed_modifier=1.3)
                        particle.z_index = random.randint(-1, 1)
                    elif self.direction == RIGHT:
                        particle = FireParticle(x=self.position.x+7, y=self.position.y+1, direction=self.direction, speed_modifier=1.3)
                        particle.z_index = random.randint(-1, 1)

        if self.state == State.SHIELDING:
            # regen fuel
            self._fuel_elapsed_time += delta
            if self.fuel < 20 and self._fuel_elapsed_time >= self._fuel_cooldown:
                self.fuel += 1
            if self.frame < 3 and self.is_shielding():
                match self.frame:
                    case 0:
                        self.texture = [
                            [*"    O  "],
                            [*" / / \\ "],
                            [*"  / \\  "]
                        ]
                    case 1:
                        self.texture = [
                            [*"     O "],
                            [*"   //\\ "],
                            [*"  / )  "]
                        ]
                    case 2:
                        if self.is_flipped:
                            self.position.x -= 1
                        self.texture = [
                            [" "],
                            [*"   .- O "],
                            [*"  / ) \\\\"]
                        ]
                self.frame += 1
                if self.direction == LEFT:
                    self.texture = text.mapfliph(self.texture)
            elif self.frame > 0 and not self.is_shielding():
                self.frame -= 1
                match self.frame:
                    case 0:
                        self.texture = [
                            [*"   O   "],
                            [*" / | \\ "],
                            [*"  / \\  "]
                        ]
                    case 1:
                        self.texture = [
                            [*"    O  "],
                            [*" / / \\ "],
                            [*"  / \\  "]
                        ]
                    case 2:
                        if self.is_flipped:
                            self.position.x += 1
                        self.texture = [
                            [*"     O "],
                            [*"   //\\ "],
                            [*"  / )  "]
                        ]
                if self.direction == LEFT:
                    self.texture = text.mapfliph(self.texture)
            elif self.frame != 3:
                self.state = State.IDLE
                self.frame = 0
                self.shield.deactivate()
            elif self.frame == 3 and not self.shield.animation.is_playing:
                if self.shield.health > 0:
                    self.shield.activate()
                if self.direction == RIGHT:
                    self.shield.set_global_position(self.get_global_position() + Vec2(9, 0))
                elif self.direction == LEFT:
                    self.shield.set_global_position(self.get_global_position() + Vec2(-2, 0))


class PlayerA(PlayerTemplate):
    def is_moving_left(self) -> bool:
        return keyboard.is_pressed("a")
    
    def is_moving_right(self) -> bool:
        return keyboard.is_pressed("d")
    
    def is_attacking(self) -> bool:
        return keyboard.is_pressed("w")
    
    def is_shielding(self) -> bool:
        return keyboard.is_pressed("s")


class PlayerB(PlayerTemplate):
    def is_moving_left(self) -> bool:
        return keyboard.is_pressed(75) # arrow left
    
    def is_moving_right(self) -> bool:
        return keyboard.is_pressed(77) # arrow right
    
    def is_attacking(self) -> bool:
        return keyboard.is_pressed(72) # arrow up
    
    def is_shielding(self) -> bool:
        return keyboard.is_pressed(80) # arrow down


class PlayerC(PlayerTemplate):
    def is_moving_left(self) -> bool:
        return keyboard.is_pressed("g")
    
    def is_moving_right(self) -> bool:
        return keyboard.is_pressed("j")
    
    def is_attacking(self) -> bool:
        return keyboard.is_pressed("y")
    
    def is_shielding(self) -> bool:
        return keyboard.is_pressed("h")
