Website Reference
=================
The different versions of AVE all use the game library on this website.
This page contains details of how to access games in this library.

gamelist.json
-------------
`http://www.avegame.co.uk/gamelist.json` contains a list of all available AVE games.
This includes both the default games and the user contributed games.
The games in this json will appear in the following format:
    [
     "title":%%string title%%,
     "author":%%string author%%,
     "desc":%%string desc%%,
     "active":%%bool active%%,
     "user":%%bool user%%,
     "filename":%%string filename%%,
     "version":%%int version%%,
     "ave_version":%%list(int) ave_version%%,
     "number":%%int number%%
    ]

%%title%%, %%author%% and %%desc%% give the title, author(s) and description of the game, taken from the `.ave` file.
%%active%% tells whether or not the game is active.
%%user%% tells whether or not the game is a user game.
%%filename%% gives the filename of the game.
%%version%% gives the version number of the game; this will probably be 1 unless the game has been changed and a new version uploaded.
%%ave_version%% gives the minimum AVE version number needed to run the game.

download/%%filename%%.ave and download/user/%%filename%%.ave
--------------------------------------------------------
`http://www.avegame.co.uk/download/%%filename%%.ave` and `http://www.avegame.co.uk/download/user/%%filename%%.ave` will give you the `.ave` 
files of the game.
