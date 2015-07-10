coverage erase
coverage run --omit=tetris_wars/sdl2/*,/home/m1trix/.local/* -m unittest discover
coverage html
coverage report
