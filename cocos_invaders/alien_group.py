"""
Alien group class
"""
from alien_column import AlienColumn

import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

class AlienGroup(object):
    def __init__(self, x, y):
        """
        Groups of alien columns, with specified characteristics
        """
        self.columns = [AlienColumn(x + i * 60, y)
                        for i in range(10)]
        self.speed = eu.Vector2(10, 0)
        self.direction = 1
        self.elapsed = 0.0
        self.period = 1.0

    def update(self, elapsed):
        """
        Move each alien based on elapsed time and the
        period.
        """
        self.elapsed += elapsed
        while self.elapsed >= self.period:
            self.elapsed -= self.period
            offset = self.direction * self.speed
            if self.side_reached():
                self.direction *= -1
                offset = eu.Vector2(0, -10)
            for alien in self:
                alien.move(offset)

    def side_reached(self):
        """
        Returns true if any of the columns should turn
        """
        return any(map(lambda c: c.should_turn(self.direction), self.columns))

    def __iter__(self):
        """
        Give an alien for each column
        """
        for column in self.columns:
            for alien in column.aliens:
                yield alien
