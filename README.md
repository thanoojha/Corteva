# LaserMirrors Problem:

## Problem Statement 

You will be given a rectangle containing square rooms in an X by Y-configuration with an open door in the center of every wall.  Some rooms will have a mirror in them at a 45-degree angle.  The mirrors may reflect off both sides (2-way mirrors) or reflect off one side and allow the beam to pass through from the other (1-way mirrors).  When the laser hits the reflective side of one of the mirrors, the beam will reflect off at a 90-degree angle.  Your challenge is to write the code to find the exit point of a laser shot into one of the open doors.  For output, you must provide the room it will be exiting through along with the orientation.  The definition file will be provided through command line parameters.

## Solution 

### Design

![Image Description](https://drive.google.com/uc?export=view&id=1Le0T7j0eSTBHd5Uls_S5BSFfijLcgI1f)


### Assumptions

- Maze dimensions provided in the input are always valid integers.
- Mirror orientations can be `RR`, `R`, `LL`, `L`.
- Laser direction can be `VE(Vertical East)`,`VW(Vertical West)`,  `HS(Horizontal South)`, `HN(Horizontal North)`.
- *Laser movement* should be within the boundaries of the maze.
- The input file is *readable* and *accessible*.
- *Laser* can start only from the boundary and not from anywhere between the maze.
- If there are `two` mirrors at the `same` position, the `first` mirror gets `ignored`.

### Class Objects

`LaserPosition` class is a *data structure* to hold the laser's position(`x`,`y`) and its direction.

  ```python
  class  LazerPosition:
	def  __init__(self, x, y, direction):
		self.x  =  x
		self.y  =  y
		self.direction  =  direction
  ```

---

`Mirror` class is a *data structure* to hold the mirror's position(`x`,`y`) and its orientation.
```python
class  Mirror:
	def  __init__(self, x, y, orientation):
		self.x  =  x
		self.y  =  y
		self.orientation  =  orientation
```
---

`Game` class initialises the game with maze dimensions (`maze_width`, `maze_height`).

```python 
class  Game:
	def  __init__(self, maze_width, maze_height):
		self.maze_height  =  maze_height
		self.maze_width  =  maze_width
		self.max_try  =  maze_height  *  maze_width  *  100
		self.current_step  =  0
		self.mirrors  =  defaultdict(lambda: defaultdict(Mirror))
		self.lazer_position  =  None
		self.game_status  =  "running"
```

-  `max_try` is a safety precaution to prevent infinite loops, setting a high limit on the number of steps.
- `current_step` is used to track the number of steps the laser has taken.
- `mirrors` is a nested *defaultdict* storing mirrors at each (`x`, `y`) position.
- `laser_position` is initialized to `None` initially and will store the laser's starting position.
- `game_status` is used to track the game state. It starts as `running`.

- `add_mirror` is used to add a mirror at position ('x', 'y') with a specific orientation.
- `add_starting_position` is used to set the initial position and direction of the laser.
- `print_dimensions` is used to print the maze dimensions (`width`, `height`).

  

`print_current_position` is used to print the laser position and the current direction of the laser to help debug and track the laser's path during the game execution.

`print_out_of_bounds` is used to print an out-of-bounds message to indicate that the laser is out of bounds with the laser position and its direction. It is helpful to handle and debug situations where the laser leaves the maze.

`print_starting_position` is used to print the starting point of the laser and the first character of its direction which would be either `H (Horizontal)` or `V(Vertical)`.

`print_exit_position` is used to print the exit position of the laser along with the direction the laser is exiting (`H` or `V`). This function first checks if the game is still running.

1) If the game is still `running`:

	i) If the status of the game is `running` and if the current step is `greater than 0`, it indicates that the laser `did not find an exit` and is in the `loop`.

	ii) If the status of the game is `running` and if the current step is `0`, it indicates that the laser has `not started yet`.

	`In the above two cases (i & ii) it returns None to exit the method`.

2) If the game is not `running`:
   	The method checks the laser's `final direction` and `prints the exit position`.

   ```python
   if self.laser_position.direction == "HN":
            print(f"Exit position: {self.laser_position.x+1}, {self.laser_position.y}, H")
   elif self.laser_position.direction == "HS":
            print(f"Exit position: {self.laser_position.x-1}, {self.laser_position.y}, H")
   elif self.laser_position.direction == "VE":
            print(f"Exit position: {self.laser_position.x}, {self.laser_position.y-1}, V")
   elif self.laser_position.direction == "VW":
            print(f"Exit position: {self.laser_position.x}, {self.laser_position.y+1}, V")

   ```
   
   ![Image Description](https://drive.google.com/uc?export=view&id=1JDYwh0x41HYauaIx_H0HLYj_q75X_LjX)
   
- If the direction of the laser is `HN` then the `x coordinate` keeps decreasing and it will be out of bounds so increase the value of `x`  by `1` to get the exit position.
- Likewise, if the direction of the laser is `HS` then the `x coordinate` keeps increasing and it will be out of bounds so decrease the value of `x`  by `1` to get the exit position.
- Likewise, if the direction of the laser is `VE` then the `y coordinate` keeps increasing and it will be out of bounds so decrease the value of `y`  by `1` to get the exit position.
- Likewise, if the direction of the laser is `VW` then the `y coordinate` keeps decreasing and it will be out of bounds so increase the value of `y`  by `1` to get the exit position.

`start` method runs the main game loop:

1) It ensures the current step does not exceed the maximum steps allowed thereby eliminating any infinite loops.

2) Increments the `current_step` by `1` for each iteration.

3) Ensure the laser's x and y coordinates are within the vertical and horizontal boundaries of the maze respectively and are non-negative.

4) Ensures that the laser's current position is within the dictionary of mirrors. If all the conditions are true then it retrieves the orientation of the mirror for further processing.

5) Based on the current direction of the laser and the orientation of the mirror, we update the direction of the laser after it interacts with the mirror:

	- if current laser position of the laser = `VE` and the orientation of the mirror = `R or RR` then the laser direction would turn `HS`
	- Likewise direction = `VE` and orientation = `L or LL` then the laser direction would turn `HN`
	- Likewise direction = `VW` and orientation = `R` then the laser direction would turn `HN`
	- Likewise direction = `VW` and orientation = `RR` then the laser direction would turn `VW`
	- Likewise direction = `VW` and orientation = `L` then the laser direction would turn `HS`
	- Likewise direction = `VW` and orientation = `LL` then the laser direction would turn `VW`
	- Likewise direction = `HS` and orientation = `RR` then the laser direction would turn `HS`
	- Likewise direction = `HS` and orientation = `R` then the laser direction would turn `VE`
	- Likewise direction = `HS` and orientation = `L or LL` then the laser direction would turn `VW`	 
	- Likewise direction = `HN` and orientation = `R or RR` then the laser direction would turn `VW`
	- Likewise direction = `HN` and orientation = `L` then the laser direction would turn `VE`
 	- Likewise direction = `HN` and orientation = `LL` then the laser direction would turn `HN` 
	
6) After getting the new direction, the position of the laser needs to be updated.

---

`get_file` method is used to open a file from a specified file path and returns the file object. If the file is not found, it catches an exception and exits the function with a `File not found` message.

---

`start_program` is the main function that initiates and runs the laser maze simulation. The main functions are file handling, parsing input, game initialization, and simulation execution.

- Reads the input from the `get_file` function and iterates over each line in the file. Removes leading and trailing whitespace from the line.
- Skips iteration if there's an empty line. Incrementing `curr` to move to the next section and continues with the next iteration if the line has `-1`.
- if `curr =0`, the line contains maze dimensions. Retrieves the dimensions and catches exceptions if there's any failure in the retrieval.
- if `curr =1`, the line contains mirror information. Retrieves the coordinates of the mirror and the orientation and adds the mirror to the `Game` in case of both `one-side` or `two-side` mirrors. Catches exceptions in case of any failures.
- if `curr = 2`, the line contains the starting position and direction of the laser. Checks for the direction of the laser and assigns the current position of the laser accordingly. Catches exceptions in case of any failures.
```python
if y[-1] == "V":
	if int(y[:-1]) == 0:
		curr_pos = [int(x), int(y[:-1]), "VE"]
	elif int(x) == n - 1:
		curr_pos = [int(x), int(y[:-1]), "VW"]
	else:
		curr_pos = [int(x), int(y[:-1]), "VW"]
elif y[-1] == "H":
	if int(x) == 0:
		curr_pos = [int(x), int(y[:-1]), "HS"]
	elif int(y[:-1]) == m - 1:
		curr_pos = [int(x), int(y[:-1]), "HN"]
	else:
		curr_pos = [int(x), int(y[:-1]), "HN"]
	
```
1) If the direction of the laser is `V`:
   - if the position is at the `right (int(y[:-1]) == 0)` then the direct would be `VE`
   - if the position is at the `left (int(x) == n - 1)` then the direct would be `VW`
2) Likewise, if the direction of the laser is `H`:
   - if the position is at the `top (int(x) == 0)` then the direct would be `HS`
   - if the position is at the `bottom (int(y[:-1]) == m - 1)` then the direct would be `HN`


TestCases
---
1) **Input should be valid**: try catch is return to handle invalid input in the code. Catches this error in the code.

```
	Input:
	5,5
	-1
	-1
	0
```
```
	Output: 
	Starting mirror simulation
	Enter file path: test.txt
	Invalid starting position
```
---
2) **Eliminating infinite loop by adding this piece of code**:

	> self.current_step < self.max_try

It indicates that the current step count doesn't exceed the maximum allowed steps. This helps to prevent infinite loops and controls the execution thereby preventing performance issues.

---
3) **Eliminating Laser out of bounds**:

Ensure the laser's x and y coordinates are within the vertical and horizontal boundaries of the maze respectively and are non-negative. This helps to handle and debug situations where the laser leaves the maze boundaries.

---
4) **Input with invalid mirror orientation**: Catches this invalid mirror orientation error in the code.
```
	Input:
	5,5
	-1
	1,1XYZ
	-1
	0,0V
```
```
	Output: 
	Starting mirror simulation
	Enter file path: test.txt
	Invalid mirror
```
5) **Input with invalid dimensions**: Catches this invalid dimension error in the code.
```
	Input:
	5,a
	-1
	1,1R
	-1
	0,0V
```
```
	Output: 
	Starting mirror simulation
	Enter file path: test.txt
	Invalid dimensions
```

---
6) **If there are multiple mirrors at the same position**: If there are `two` mirrors at the `same` position, the `first` mirror gets `ignored`.

```
	Input:
	5,5
	-1
	1,1R
	1,1L
	-1
	0,0H
```
```
	Output: 
	Enter file path: test.txt
	Dimensions: 5, 5
	Starting position: 0, 0, H
	Exit position: 4, 0, H
```

---
7) **Input with invalid laser starting position**: Catches this invalid laser starting position error in the code.
```
	Input:
	5,5
	-1
	1,1R
	-1
	0,aH
```
```
	Output: 
	Starting mirror simulation
	Enter file path: test.txt
	Invalid starting position
```

---
8) **Input with no mirrors**:

```
	Input:
	5,5
	-1
	-1
	0,0H
```
```
	Output: 
	Starting mirror simulation
	Enter file path: test.txt
	Dimensions: 5, 5
	Starting position: 0, 0, H
	Exit position: 4, 0, H
```
  
  

## Execution:

### Prerequisite 
- Python3 
- VS Code or any code editor. 
- `Test.txt` file.

### Run command
 `python3 main.py` 

