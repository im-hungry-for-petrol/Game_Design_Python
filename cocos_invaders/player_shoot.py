"""
Based off of the Shoot class
"""
from shoot import Shoot
from alien import Alien

class PlayerShoot(Shoot):
    INSTANCE = None

    def __init__(self, x, y):
        """
        Sets the image, speed, and instance
        """
        super(PlayerShoot, self).__init__(x, y, 'img/laser.png')
        self.speed *= -1
        PlayerShoot.INSTANCE = self

    def collide(self, other):
        """
        Check if it has collided with an alien, if so,
        update the score and delete both entities.
        """
        if isinstance(other, Alien):
            self.parent.update_score(other.score)
            other.kill()
            self.kill()

    def on_exit(self):
        """
        Change instances and remove from field.
        """
        super(PlayerShoot, self).on_exit()
        PlayerShoot.INSTANCE = None
