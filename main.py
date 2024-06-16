from collections import defaultdict

#Data Structure to hold laser's position and direction
class LaserPosition:
    def __init__(self, x, y, direction):
        self.x = x 
        self.y = y 
        self.direction = direction

# Data Structure to hold the mirror's position and orientation
class Mirror:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation

# Game class initializes the game with maze dimensions
class Game:
    def __init__(self, maze_width, maze_height):
        self.maze_height = maze_height
        self.maze_width = maze_width
        self.max_try = maze_height * maze_width * 100
        self.current_step = 0
        self.mirrors = defaultdict(lambda: defaultdict(Mirror))
        self.laser_position = None
        self.game_status = "running"
    
    # adding mirrors at (x,y) position with specific orientation
    def add_mirror(self, x, y, orientation):
        self.mirrors[x][y] = Mirror(x, y, orientation)
    
    # setting the initial position and the direction of the laser
    def add_starting_position(self, x,y, direction):
        self.laser_position = LaserPosition(x, y, direction)
    
    # printing maze dimensions
    def print_dimensions(self):
        print(f"Dimensions: {self.maze_width}, {self.maze_height}")

    # printing current laser position
    def print_current_position(self):
        print(f"Current position: {self.laser_position.x}, {self.laser_position.y}, {self.laser_position.direction}")
    
    # printing out of bounds position
    def print_out_of_bounds(self):
        print(f"Out of bound: {self.laser_position.x}, {self.laser_position.y}, {self.laser_position.direction}")

    # printing starting position of the laser and its direction
    def print_starting_position(self):
        print(f"Starting position: {self.laser_position.x}, {self.laser_position.y}, {self.laser_position.direction[0]}")

    # printing exit position of the laser and its direction
    def print_exit_position(self):
        if self.game_status == "running":
            if self.current_step > 0:
                print("Laser did not exit maze, in loop")
            else:
                print("Laser yet to start")
            return None
        
        if self.laser_position.direction == "HN":
            print(f"Exit position: {self.laser_position.x+1}, {self.laser_position.y}, H")
        elif self.laser_position.direction == "HS":
            print(f"Exit position: {self.laser_position.x-1}, {self.laser_position.y}, H")
        elif self.laser_position.direction == "VE":
            print(f"Exit position: {self.laser_position.x}, {self.laser_position.y-1}, V")
        elif self.laser_position.direction == "VW":
            print(f"Exit position: {self.laser_position.x}, {self.laser_position.y+1}, V")



    def start(self):
        # Eliminating infinite loops
        while True and self.current_step < self.max_try:
            self.current_step += 1
            # self.print_current_position()

            # Checking if the laser is out of bounds
            if self.laser_position.x >= self.maze_height or self.laser_position.y >= self.maze_width or self.laser_position.x < 0 or self.laser_position.y < 0:
                # self.print_out_of_bounds()
                self.game_status = "ended"
                break

            # If the laser encounters a mirror, it changes direction based on the mirror's orientation and laser direction
            if self.laser_position.x in self.mirrors and self.laser_position.y in self.mirrors[self.laser_position.x] and self.mirrors[self.laser_position.x][self.laser_position.y].orientation in  ["RR", "R", "L", "LL"]:
                turn = self.mirrors[self.laser_position.x][self.laser_position.y].orientation
                print("turn", turn)
                if self.laser_position.direction == "VE" and turn == "R":
                    self.laser_position.direction = "HS"
                elif self.laser_position.direction == "VE" and turn == "RR":
                    self.laser_position.direction = "HS"
                elif self.laser_position.direction == "VE" and turn == "LL":
                    self.laser_position.direction = "HN"
                elif self.laser_position.direction == "VE" and turn == "L":
                    self.laser_position.direction = "HN"
                elif self.laser_position.direction == "VW" and turn == "R":
                    self.laser_position.direction = "HN"
                elif self.laser_position.direction == "VW" and turn == "RR":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "VW" and turn == "LL":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "VW" and turn == "L":
                    self.laser_position.direction = "HS"
                elif self.laser_position.direction == "HS" and turn == "R":
                    self.laser_position.direction = "VE"
                elif self.laser_position.direction == "HS" and turn == "RR":
                    self.laser_position.direction = "HS"
                elif self.laser_position.direction == "HS" and turn == "LL":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "HS" and turn == "L":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "HN" and turn == "R":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "HN" and turn == "RR":
                    self.laser_position.direction = "VW"
                elif self.laser_position.direction == "HN" and turn == "LL":
                    self.laser_position.direction = "HN"
                elif self.laser_position.direction == "HN" and turn == "L":
                    self.laser_position.direction = "VE"

                =

            # updating the laser's position based on its direction
            if self.laser_position.direction == "VE":
                self.laser_position.y += 1
            elif self.laser_position.direction == "VW":
                self.laser_position.y -= 1
            elif self.laser_position.direction == "HS":
                self.laser_position.x += 1
            elif self.laser_position.direction == "HN":
                self.laser_position.x -= 1

# Reading the input file
def get_file(file_path):
    try:
        file = open(file_path, "r")
    except FileNotFoundError:
        print("File not found")
        return
    return file

# Main function that initiates and runs the laser maze simulation
def start_program():
    # entering file path
    file = get_file(input("Enter file path: "))
    curr = 0
    game = None
    # Iterate over each line in the file
    for line in file.readlines():
        line = line.strip() #removes leading and trailing whitespace from the line
        # Skipping iteration if there's an empty line
        if line == "":
            continue
        # Incrementing curr to move to the next section and continues with next iteration if line has -1
        if line == "-1":
            curr += 1
            continue

        # if curr =0, the line contains maze dimenions
        if curr == 0:
            try:
                # mapping the values to m and n
                m,n = list(map(int, line.split(",")))
                game = Game(m, n)
                # catching errors related to invalid dimensions
            except ValueError:
                print("Invalid dimensions")
                return
            
        # if curr =1, the line contains mirror information
        elif curr == 1:
            try:
                x, y = line.split(",")
                # extracting mirror orientation
                last = y[-1]
                last_last = y[-2]
                #extracting coordinates and orientation for one way mirror
                if last_last.isnumeric():
                    # checking game initialization
                    if game is None:
                        print("Game not initialized")
                        return
                    game.add_mirror(int(x), int(y[:-1]), last.upper())
                #extracting coordinates and orientation for two way mirror
                else:
                    if game is None:
                        print("Game not initialized")
                        return
                    game.add_mirror(int(x), int(y[:-2]), last_last.upper() + last.upper())
            except ValueError:
                print("Invalid mirror")
                return
            
         # if curr = 2, the line contains starting position and direction of the laser
        elif curr == 2:
            try:
                x, y = line.split(",")
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
                if game is None:
                    print("Game not initialized")
                    return
                game.add_starting_position(curr_pos[0], curr_pos[1], curr_pos[2])
            except ValueError:
                print("Invalid starting position")
                return

    file.close()
    game.print_dimensions()
    game.print_starting_position()
    game.start()
    game.print_exit_position()

if __name__ == "__main__":
    print("Starting mirror simulation")
    start_program()