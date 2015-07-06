class Settings:

    def __init__(self):
        self.grid_width = 10
        self.grid_height = 22

        self.queue_size = 0
        self.tetrimino_repetition_limit = 2

        self.game_speed = 0.25
        self.soft_drop_speed = 0.05
        self.line_clear_speed = 0.20

        self.use_gravity = True
        self.gravity_speed = 0.25

        self.use_easy_spin = True
        self.easy_spin_limit = 20
        self.easy_spin_timeout = 0.50
