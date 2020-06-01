"""
The actor class, base class for all sprites.
"""
import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        """
        Initializing with an image and a position
        """
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position,
                                    self.width * 0.5,
                                    self.height * 0.5)

    def move(self, offset):
        """
        Simple movement based on an offset.
        """
        self.position += offset
        self.cshape.center += offset

    def update(self, elapsed):
        """
        To be overridden
        """
        pass

    def collide(self, other):
        """
        To be overridden
        """
        pass
