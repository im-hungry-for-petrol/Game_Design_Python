"""
Shoot class
"""
from actor_2 import Actor

import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class Shoot(Actor):
    def __init__(self, x, y, img='img/shoot.png'):
        """
        Initializing with proper images and stuff
        """
        super(Shoot, self).__init__(img, x, y)
        self.speed = eu.Vector2(0, -400)

    def update(self, elapsed):
        """
        Moving the shoot 
        """
        self.move(self.speed * elapsed)
