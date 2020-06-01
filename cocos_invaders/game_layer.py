"""
June 1, 2020
Main file for running the cocos invaders
"""

import cocos.layer
from player_cannon import PlayerCannon
from alien import Alien
from alien_column import AlienColumn
from alien_group import AlienGroup
from player_shoot import PlayerShoot
from shoot import Shoot
from hud import HUD
from mystery_ship import MysteryShip

import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu
import random

class GameLayer(cocos.layer.Layer):
    """
    The main layer where the player will interact with the enemies.
    """
    is_event_handler = True

    def on_key_press(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 0

    def __init__(self, hud):
        """
        Creating the player, defining cells, beginning
        schedule/update for constant movements.
        """
        super(GameLayer, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.hud = hud
        self.width = w
        self.height = h
        self.lives = 3
        self.score = 0
        self.update_score()
        self.create_player()
        self.create_alien_group(100, 300)
        cell = 1.25 * 50
        self.collman = cm.CollisionManagerGrid(0, w, 0, h, cell, cell)
        self.schedule(self.update)

    def create_player(self):
        """
        Placing the player cannon in the layer.
        """
        self.player = PlayerCannon(self.width * 0.5, 50)
        self.add(self.player)
        self.hud.update_lives(self.lives)

    def update_score(self, score=0):
        """
        Updating the score on the HUD
        """
        self.score += score
        self.hud.update_score(self.score)

    def create_alien_group(self, x, y):
        """
        Adding aliens by group
        """
        self.alien_group = AlienGroup(x, y)
        for alien in self.alien_group:
            self.add(alien)

    def update(self, dt):
        """
        Responsible for constantly updating the position of the
        aliens/playercannon/etc
        """
        # adding objects to the collision manager
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
            if not self.collman.knows(node):
                self.remove(node)

        # check if player has collided
        self.collide(PlayerShoot.INSTANCE)
        if self.collide(self.player):
            self.respawn_player()

        # let aliens shoot when the laser is gone
        for column in self.alien_group.columns:
            shoot = column.shoot()
            if shoot is not None:
                self.add(shoot)

        # update each node after adding everything
        for _, node in self.children:
            node.update(dt)
        self.alien_group.update(dt)

        # deploy mystery ship at random intervals
        if random.random() < 0.001:
            self.add(MysteryShip(50, self.height - 50))

    def respawn_player(self):
        """
        Called upon damage, decrements life and determines
        whether it should be gameover.
        """
        self.lives -= 1
        if self.lives < 0:
            self.unschedule(self.update)
            self.hud.show_game_over()
        else:
            self.create_player()

    def collide(self, node):
        """
        Checks if a specified node has collided with another
        object on the field. Return true/false.
        """
        if node is not None:
            for other in self.collman.iter_colliding(node):
                node.collide(other)
                return True
        return False

if __name__ == '__main__':
    """
    Initializing respective layers and running the game.
    """
    cocos.director.director.init(caption='Cocos Invaders',
                                width=1000, height=650)
    main_scene = cocos.scene.Scene()
    hud_layer = HUD()
    main_scene.add(hud_layer, z=1)
    game_layer = GameLayer(hud_layer)
    main_scene.add(game_layer, z=0)
    cocos.director.director.run(main_scene)
