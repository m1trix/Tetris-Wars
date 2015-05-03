class Controller:

    def __init__(self, engine):
        self.__engine = engine

    def press(self, key):
        if key == "left":
            self.__engine.tetrimino.move_hor(-1)
        else:
            return None

        self.__engine.renderer.render()