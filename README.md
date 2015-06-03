# Tetris-Wars

### Description
It's a classic game of Tetris.

### Usage
The game is started by executing ``` python3 tetris_wars/main.py ```

### Architecture
##### Engine
The main component of the game is the Engine class. It has a single ``` execute() ``` method which runs a game, until it's over. The parameters of that execution are given when the instance is created, by providing a Settings instance as a parameter to the constructor.

The Engine class uses only four classes to run the whole game:
* **GameCore** - holds the basic mechanics of the game;
* **Controller** - invokes given methods of the game core according to the user input;
* **RendererCore** - creates 'snapshots' of the game that are rendered;
* **Timer** - determines when certain events must be executed by the engine.

##### GameCore
The class handles the Tetris specific logic. It progresses the game, calculates the position of the ghost tetrimino, generates new tetrimino when the current one hits the ground. It completely exposes the Tetrimino object that it holds.

##### Controller
The class takes a list of Action instances and executes them by taking the elements of the GameCore and passing them to given utility classes.

##### RendererCore
The class wraps the GameCore instance of the engine and only provides copies of its fields. This enables the creation of custom Renderer classes but prevents a missusage of the GameCore isntance.

##### Timer
The class basically counts the time. The Engine class invokes the ``` wait() ``` method, which blocks it, until the timer hits 0. That can happen in one of two ways: by waiting a given amount of time or by invoking the ``` reset() ``` method of the Timer instance (usually from another thread). The ``` reset() ``` enables some class (e.g. Controller) to force progress of the game, without having any acces to the Engine class.
