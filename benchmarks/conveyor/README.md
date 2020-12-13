# To create the game:

```python3 game.py > game_file.txt```

The output should first list the state numbers and whose turn it is (0 for human, 1 for robot)

Then there is a list of (state, state, reward) tuples.


# To modify the game:

Change config_file.py

Of interest:

Change the size:
Width is the number of cells in each row of the conveyor belt.

Length is the number of rows. Note that the last row is used to model objects that have fallen off the belt.

Insertion frequency is unused (currently blocks are replaced the turn after they are removed to keep the number of blocks constant)

Speed is the distance objects move each time step. (currently not used)


Time is relative to the speed of the belt (the objects move down one cell per unit time)
Robot speed is the number of cells the robot moves in one step
Human speed is the number of cells the human moves in one step