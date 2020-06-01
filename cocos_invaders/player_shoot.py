from shoot import Shoot
from alien import Alien

class PlayerShoot(Shoot):
    INSTANCE = None

    def __init__(self, x, y):
        super(PlayerShoot, self).__init__(x, y, 'img/laser.png')
        self.speed *= -1
        PlayerShoot.INSTANCE = self

    def collide(self, other):
        if isinstance(other, Alien):
            self.parent.update_score(other.score)
            other.kill()
            self.kill()

    def on_exit(self):
        super(PlayerShoot, self).on_exit()
        PlayerShoot.INSTANCE = None
