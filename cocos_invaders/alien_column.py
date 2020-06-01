from alien import Alien
from shoot import Shoot

import random

class AlienColumn(object):
    def __init__(self, x, y):
        """
        Constructs a column of aliens
        """
        alien_types = enumerate(['3', '3', '2', '2', '1'])
        self.aliens = [Alien.from_type(x, y+i*60, alien, self)
                for i, alien in alien_types]

    def remove(self, alien):
        """
        Removes an alien
        """
        self.aliens.remove(alien)

    def shoot(self):
        """
        Shoot at random intervals
        """
        if random.random() < 0.001 and len(self.aliens) > 0:
            pos = self.aliens[0].position
            return Shoot(pos[0], pos[1] - 50)
        return None

    def should_turn(self, d):
        """
        Determines if the aliens have hit the border and if they
        should turn
        """
        if len(self.aliens) == 0:
            return False
        alien = self.aliens[0]
        x, width = alien.x, alien.parent.width
        return x >= width - 50 and d == 1 or x <= 50 and d == -1
