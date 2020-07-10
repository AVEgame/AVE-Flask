Running AVE on Windows
======================
Before running AVE on Windows, you will need to [install Python](https://www.python.org/downloads/).

Installing AVE using Pip
------------------------
To install AVE using pip, open command prompt by typing "cmd" in your start menu. Then run:
    py -m pip install avegame

Once AVE has installed, you can play games by running the following command in command prompy:
    ave

If you want to load games you own games from a folder as well as the build in games, you can run:
    ave /path/to/folder

Downloading the source
----------------------
You can download AVE from [GitHub](/git).

Before running AVE, you will need to install `windows-curses`:
    py -m pip install windows-curses

You can then run AVE by navigating to the directory it is installed in and running:
    py run.py

We recommend doing this if you want to write your own AVE game, as you can then simply place you game in the `games` folder, then run AVE to test your game.
