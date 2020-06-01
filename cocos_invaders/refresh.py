import cocos
from actor import Actor
from collections import defaultdict
from pyglet.window import key

import cocos
import cocos.collision_model as cm
import cocos.euclid as eu

class MainLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MainLayer, self).__init__()
        self.player = Actor(320, 240, (0, 0, 255))
        self.add(self.player)
        for pos in [(100, 100), (540, 380), \
                (540, 100), (100,380)]:
            self.add(Actor(pos[0], pos[1], (255, 0, 0)))

        cell = self.player.width * 1.25
        self.collman = cm.CollisionManagerGrid(0, 640, 0, 480, cell, cell)

        self.speed = 100.0
        self.pressed = defaultdict(int)
        self.schedule(self.update)

    def on_key_press(self, k, m):
        self.pressed[k] = 1

    def on_key_release(self, k, m):
        self.pressed[k] = 0

    def update(self, dt):
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)
        for other in self.collman.iter_colliding(self.player):
            self.remove(other)

        x = self.pressed[key.RIGHT] - self.pressed[key.LEFT]
        y = self.pressed[key.UP] - self.pressed[key.DOWN]
        if x != 0 or y != 0:
            pos = self.player.position
            new_x = pos[0] + self.speed * x * dt
            new_y = pos[1] + self.speed * y * dt
            self.player.position = (new_x, new_y)
            self.player.cshape.center = self.player.position

if __name__ == '__main__':
    cocos.director.director.init(caption='Poopie pee pee')
    layer = MainLayer()
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)
