"""
May 31, 2020
"""

import tkinter as tk
from item_classes import GameObject, Paddle, Ball, Brick

class Game(tk.Frame):
    """
    Main class for the PONG game.
    """
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400

        # the canvas is where everything happens
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()

        # initializing objects
        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        # adding user control
        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                        lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                        lambda _: self.paddle.move(10))

    def setup_game(self):
        """
        Start screen, press start to begin
        """
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200,
        'Press space to start.')
        self.canvas.bind('<space>',
        lambda _: self.start_game())

    def add_ball(self):
        """
        This adds the ball based on the paddle position because
        the ball may be added after the paddle has moved.
        """
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        """
        Method to add bricks.
        """
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        """
        Method for drawing text to the screen.
        """
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        """
        Remains in upper-lefthand corner to tell how many
        lives are available.
        """
        text = 'Lives %s' % self.lives
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        """
        Space bar can no longer be used (prevents additional instances
        of game), game_loop is called.
        """
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        """
        Determine whether player has won or lost based on the amount
        of bricks/position of the ball.
        """
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None
            self.draw_text(300, 200, 'YOU WIN!')
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over.')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        """
        Find which objects are colliding with the ball.
        """
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items \
            if x in self.items]
        self.ball.collide(objects)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Sad Pong')
    game = Game(root)
    game.mainloop()
