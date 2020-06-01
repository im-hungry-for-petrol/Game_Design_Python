"""
An actor with control by the player.
"""
from collections import defaultdict
from pyglet.window import key
from actor_2 import Actor
from player_shoot import PlayerShoot

import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class PlayerCannon(Actor):
    KEYS_PRESSED = defaultdict(int)

    def __init__(self, x, y):
        """
        Setting speed, image, etc
        """
        super(PlayerCannon, self).__init__('img/cannon.png', x, y)
        self.speed = eu.Vector2(200, 0)

    def update(self, elapsed):
        """
        Add the player if space bar is pressed, otherwise use
        the move method from actor class to move based on key press.
        """
        pressed = PlayerCannon.KEYS_PRESSED
        space_pressed = pressed[key.SPACE] == 1
        if PlayerShoot.INSTANCE is None and space_pressed:
            self.parent.add(PlayerShoot(self.x, self.y + 50))

        movement = pressed[key.RIGHT] - pressed[key.LEFT]
        if movement != 0:
            self.move(self.speed * movement * elapsed)

    def collide(self, other):
        """
        If playercannon collides with another object, player cannon
        (and the other object) DIES
        """
        other.kill()
        self.kill()
