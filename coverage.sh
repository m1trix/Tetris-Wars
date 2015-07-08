coverage erase
coverage run --omit=tetris_wars/sdl2/* -m unittest discover
coverage html
coverage report -m
