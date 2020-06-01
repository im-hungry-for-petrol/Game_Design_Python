import cocos

from pyglet.window import key

class MainLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MainLayer, self).__init__()
        self.player = cocos.sprite.Sprite('ball.png')
        self.player.color = (0, 0, 255)
        self.player.position = (320, 240)
        self.add(self.player)

    def on_key_press(self, k, m):
        print('Pressed', key.symbol_string(k))

    def on_key_release(self, k, m):
        print('Released', key.symbol_string(k))

if __name__ == '__main__':
    cocos.director.director.init(caption='Hello, Cocos')
    layer = MainLayer()
    scene = cocos.scene.Scene(layer)
    cocos.director.director.run(scene)
