Full AVE language reference
===========================

Preamble
--------

| Characters | Property                          |
| ---------- | --------------------------------- |
| `==`       | Name                              |
| `--`       | Description                       |
| `**`       | Author                            |
| `@@`       | Position of the game in library   |
| `vv`       | Set the game version number (int) |
| `::`       | Set the minimum AVE version       |
| `~~`       | `~~ off ~~` disables the game     |

Rooms
-----

| Example      | Effect                           |
| ------------ | -------------------------------- |
| `# roomname` | Start a room with id `roomname`  |

| Example                           | Effect                                                           |
| --------------------------------- | ---------------------------------------------------------------- |
| `text => roomname`                | Give the user the option `text` to go to `roomname`              |
| `text => __R__(room1,room2)`      | Go randomly to `room1` or `room2`                                |
| `text => __R__(room1,room2)[4,1]` | Go randomly to `room1` or `room2` with probabilities 4/5 and 1/5 |

| Example        | Effect                   |
| -------------- | ------------------------ |
| `__GAMEOVER__` | Send to "game over" page |
| `__WINNER__`   | Send to "you win" page   |

Items
-----

| Example      | Effect                           |
| ------------ | -------------------------------- |
| `% itemname` | Start an item with id `itemname` |


| Example              | Effect                               |
| -------------------- | ------------------------------------ |
| ` + itemname`        | Add item `itemname`                  |
| ` ~ itemname`        | Remove item `itemname`               |
| ` ? itemname`        | If player has `itemname`             |
| ` ?! itemname`       | If player doesn't have `itemname`    |
| ` ? (item1 item2)`   | If player has `item1` or `item2`     |
| ` ? (item1 !item2)`  | If player has `item1` or not `item2` |

Number items
------------

| Example         | Effect                                                       |
| --------------- | ------------------------------------------------------------ |
| `__NUMBER__`    | Set the item to be a numerical variable                      |
| `__NUMBER__(4)` | Set the item to be a numerical variable with initial value 4 |

| Example          | Effect                                      |
| ---------------- | ------------------------------------------- |
| ` + itemname`    | Add one to `itemname`                       |
| ` + itemname=4`  | Set `itemname` equal to 4                   |
| ` + itemname+4`  | Add 4 to `itemname`                         |
| ` + itemname-4`  | Take 4 from `itemname`                      |
| ` ~ itemname`    | Take one from `itemname`                    |
| ` ? itemname`    | If `itemname` is greater than 0             |
| ` ?! itemname`   | If `itemname` is 0                          |
| ` ? itemname==4` | If `itemname` is 4                          |
| ` ? itemname>=4` | If `itemname` is greater than or equal to 4 |

| Example      | Effect                                |
| ------------ | ------------------------------------- |
| `$itemname$` | Include the number `itemname` in text |

| Example     | Effect                           |
| ----------- | -------------------------------- |
| `__R__`     | A random number between 0 and 1  |
| `__R__(10)` | A random number between 0 and 10 |

Other
-----

| Example        | Effect                                    |
| -------------- | ----------------------------------------- |
| `<newline>`    | Include a newline                         |
| `<|` ... `|>`  | Escape text                               |
