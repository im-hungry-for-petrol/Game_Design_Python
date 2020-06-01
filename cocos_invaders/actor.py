import cocos
from collections import defaultdict
from pyglet.window import key
import cocos.euclid as eu
import cocos.collision_model as cm

class Actor(cocos.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Actor, self).__init__('ball.png', color=color)
        self.position = pos = eu.Vector2(x, y)
        self.cshape = cm.CircleShape(pos, self.width/2)
