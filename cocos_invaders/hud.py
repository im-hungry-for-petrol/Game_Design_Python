"""
HUD class, additional layer overlaying the others.
"""
import cocos.layer

class HUD(cocos.layer.Layer):
    def __init__(self):
        """
        Adding text in respective positions
        """
        super(HUD, self).__init__()
        w, h = cocos.director.director.get_window_size()
        self.score_text = cocos.text.Label('', font_size=18)
        self.score_text.position = (20, h - 40)
        self.lives_text = cocos.text.Label('', font_size=18)
        self.lives_text.position = (w - 100, h - 40)
        self.add(self.score_text)
        self.add(self.lives_text)

    def update_score(self, score):
        """
        Change score text
        """
        self.score_text.element.text = 'Score: %s' % score

    def update_lives(self, lives):
        """
        Change lives text
        """
        self.lives_text.element.text = 'Lives %s' % lives

    def show_game_over(self):
        """
        Display gameover text 
        """
        w, h = cocos.director.director.get_window_size()
        game_over = cocos.text.Label('Game Over', font_size=50,
                                    anchor_x='center',
                                    anchor_y='center')
        game_over.position = w * 0.5, h * 0.5
        self.add(game_over)
