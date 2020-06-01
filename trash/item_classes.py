class GameObject(object):
    """
    Base class for other objects. The methods
    are fairly obvious.
    """
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)

class Paddle(GameObject):
    """
    Paddle class, for deflecting the ball and user control.
    """
    def __init__(self, canvas, x, y):
        """
        Creating the paddle with its starting positions.
        """
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width/2,
                                       y - self.height/2,
                                       y + self.width/2,
                                       y + self.height/2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        """
        Defining which ball works with the paddle.
        """
        self.ball = ball

    def move(self, offset):
        """
        Move the paddle based on an offset value.
        """
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and \
            coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)

class Brick(GameObject):
    """
    Class for defining a brick.
    """
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        """
        Setting brick positions, color, etc.
        """
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width/2,
                                       y - self.height/2,
                                       x + self.width/2,
                                       y + self.height/2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        """
        Bricks change color/disappear the more that they are hit.
        """
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])

class Ball(GameObject):
    """
    Class for a ball object.
    """
    def __init__(self, canvas, x, y):
        """
        Initializing basic characteristics of the ball.
        """
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

    def update(self):
        """
        Updating the positions of the ball based on its position
        relative to other boundaries
        """
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        """
        Accepts other game_objects and determines how to change the
        direction of the ball relative to the other game objects.
        """
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()
