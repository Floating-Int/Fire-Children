from displaylib import *
import keyboard
from player import PlayerA, PlayerB, PlayerC
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
        self.player1 = PlayerA(x=3, y=3, label_position=Vec2(3, 0))
        self.player2 = PlayerB(skin=color.MEDIUM_PURPLE, x=55, y=3, label_position=Vec2(55, 0))
        self.players = [self.player1, self.player2]
        # self.audio_stream_player = AudioStreamPlayer("./audio/song.wav")
        # self.audio_stream_player.play()
        # self.player3 = PlayerC(x=15, y=self.screen.height-4, label_position=Vec2(self.screen.width // 2 -3, 1))
        # self.players = [self.player1, self.player2, self.player3]
        # self.player2.position.x = 23

    def _update(self, delta: float) -> None:
        if keyboard.is_pressed("q"):
            self.is_running = False
        # if keyboard.is_pressed("e"):
        #     print(Node.nodes)
        
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
