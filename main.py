from displaylib import * # type: ignore
import keyboard
from player import PlayerTemplate, PlayerA, PlayerB
from ground import Ground
from fire import FireParticle
from shield import Shield


class App(Engine):
    def _on_start(self) -> None:
        # -- config
        Screen.cell_default = " "
        Screen.cell_transparant = " "
        # -- camera config
        Camera.current.mode = Camera.CENTERED
        Camera.current.set_global_position(Vec2(32, 4))
        # -- nodes
        self.ground = Ground(y=6)
        self.player1 = PlayerA(x=3, y=3, label_position=Vec2(3, 0), device_index=0).as_unique()
        self.player2 = PlayerB(x=55, y=3, label_position=Vec2(55, 0), device_index=1).as_unique()
        self.players: list[PlayerTemplate] = [self.player1, self.player2]

    def _update(self, delta: float) -> None:
        if keyboard.is_pressed("q"):
            self.is_running = False
        
        for particle in FireParticle.particles:
            broke = False
            for shield in Shield.shields:
                if not shield.is_deployed:
                    continue
                if shield.get_global_position() <= particle.get_global_position() < shield.get_global_position() + Vec2(1, 4):
                    particle.queue_free()
                    broke = True
                    if shield.health > 0:
                        shield.elapsed_time = 0
                        shield.health -= 1
                        if shield.health == 0:
                            shield.deactivate()
                    break
            if broke:
                continue
            for player in self.players:
                if player.get_global_position() <= particle.get_global_position() < player.get_global_position() + Vec2(7, 3):
                    player.health -= 1
                    if player.health <= 0:
                        player.queue_free()
                        self.players.remove(player)
                    particle.queue_free()
        for shield in Shield.shields:
            shield.elapsed_time += delta
            if shield.elapsed_time >= shield.regen_delay:
                if shield.health < 15:
                    shield.health += 1


if __name__ == "__main__":
    app = App(tps=12, width=64, height=8, auto_resize_screen=True)
