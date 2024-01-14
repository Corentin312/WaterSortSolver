# WaterSortSolver
Solve Water Sort game on tablet

`game.py` is the file managing the game. The initial position is stored in this file. \
The game can handle the case when the game only shows the color at the top of a tube, using -1 as unknown. \
`solver.py` is the file solving. It writes the solution in files/solution.txt. \
\
For the automatic solver, you need to install Android Studio to screenshot and press on the tablet. You should then add `$ANDROID_HOME$/platform-tools` to your path. \
`main.py` is the file to run the automatic solving. \
The tubes coordinates and the color code are hard-coded. You might need to change it using `getcoords.py` and the `getcolor.py` to help you.
