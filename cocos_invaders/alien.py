"""
Alien class based on Actor class
"""
from pyglet.image import load, ImageGrid, Animation
from actor_2 import Actor

class Alien(Actor):
    def load_animation(imgage):
        """
        Animation for each image
        """
        seq = ImageGrid(load(imgage), 2, 1)
        return Animation.from_image_sequence(seq, 0.5)

    TYPES = {
        '1' : (load_animation('img/alien1.png'), 40),
        '2' : (load_animation('img/alien2.png'), 20),
        '3' : (load_animation('img/alien3.png'), 10)
    }

    def from_type(x, y, alien_type, column):
        """
        Change the way the alien looks based on the score
        """
        animation, score = Alien.TYPES[alien_type]
        return Alien(animation, x, y, score, column)

    def __init__(self, img, x, y, score, column=None):
        """
        Setting up the alien with its score/column
        """
        super(Alien, self).__init__(img, x, y)
        self.score = score
        self.column = column

    def on_exit(self):
        """
        Removing the alien from its respective places
        """
        super(Alien, self).on_exit()
        if self.column:
            self.column.remove(self)
