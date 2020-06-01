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
    is_event_handler = True

    def on_key_press(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 1

    def on_key_release(self, k, _):
        PlayerCannon.KEYS_PRESSED[k] = 0

    def __init__(self, hud):
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
        self.player = PlayerCannon(self.width * 0.5, 50)
        self.add(self.player)
        self.hud.update_lives(self.lives)

    def update_score(self, score=0):
        self.score += score
        self.hud.update_score(self.score)

    def create_alien_group(self, x, y):
        self.alien_group = AlienGroup(x, y)
        for alien in self.alien_group:
            self.add(alien)

    def update(self, dt):
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
            if not self.collman.knows(node):
                self.remove(node)

        self.collide(PlayerShoot.INSTANCE)
        if self.collide(self.player):
            self.respawn_player()
        for column in self.alien_group.columns:
            shoot = column.shoot()
            if shoot is not None:
                self.add(shoot)

        for _, node in self.children:
            node.update(dt)
        self.alien_group.update(dt)

        if random.random() < 0.001:
            self.add(MysteryShip(50, self.height - 50))

    def respawn_player(self):
        self.lives -= 1
        if self.lives < 0:
            self.unschedule(self.update)
            self.hud.show_game_over()
        else:
            self.create_player()

    def collide(self, node):
        if node is not None:
            for other in self.collman.iter_colliding(node):
                node.collide(other)
                return True
        return False

if __name__ == '__main__':
    cocos.director.director.init(caption='Cocos Invaders',
                                width=1000, height=650)
    main_scene = cocos.scene.Scene()
    hud_layer = HUD()
    main_scene.add(hud_layer, z=1)
    game_layer = GameLayer(hud_layer)
    main_scene.add(game_layer, z=0)
    cocos.director.director.run(main_scene)
