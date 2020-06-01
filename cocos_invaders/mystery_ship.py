"""
Mystery ship class, based off of alien
"""
from alien import Alien
import random

import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class MysteryShip(Alien):
    SCORES = [10, 50, 100, 200]

    def __init__(self, x, y):
        """
        Chooses a random score, intializing image/speed
        """
        score = random.choice(MysteryShip.SCORES)
        super(MysteryShip, self).__init__('img/alien4.png', x, y, score)
        self.speed = eu.Vector2(150, 0)

    def update(self, elapsed):
        """
        Update position 
        """
        self.move(self.speed * elapsed)
