class Settings:

    def __init__(self):
        self._settings = {
            'grid': {
                'width': 10,
                'height': 22
            },
            'generator': {
                'queue_size': 5,
                'repetition_limit': 2
            },
            'game': {
                'speed': 0.25,
                'soft_drop_speed': 0.05,
                'line_clear_speed': 0.20
            },
            'gravity': {
                'use': True,
                'speed': 0.25
            },
            'easy_spin': {
                'use': True,
                'limit': 20,
                'timeout': 0.50
            }
        }

    def __getitem__(self, key):
        return self._settings[key]
