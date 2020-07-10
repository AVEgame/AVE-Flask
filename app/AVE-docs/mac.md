Running AVE on Mac
==================
AVE was first written in Python to run in terminal in Linux and Mac.

Installing AVE using Pip
------------------------
To install AVE using pip, run the following in terminal:
    pip install avegame

You may need to use `sudo`:
    sudo pip install avegame

Or you may need to use `pip3`:
    pip3 install avegame
    sudo pip3 install avegame

Once AVE has installed, you can play games by running the following command in terminal:
    ave

If you want to load games you own games from a folder as well as the build in games, you can run:
    ave /path/to/folder

Downloading the source
----------------------
You can download AVE from [GitHub](/git). You can then run AVE by navigating to the directory it is installed in and running:
    python run.py

We recommend doing this if you want to write your own AVE game, as you can then simply place you game in the `games` folder, then run AVE to test your game.
