import turtle


exits = ["t","b","l","r"]
top = (-144, 288)
bottom = (24, -336)
left = (-288, 0)
right = (288, -24)

my_obstacles = []
walls = []
path = []

ninja = []
start_x = 0
start_y = 0
end_x = 0
end_y = 0

maze = [
"XXXXXXtXXXXXXXXXXXXXXXXXX",
"XXXXXX XXXXXXXXXXXXXXXXXX",
"XX  XX                 XX",
"XX  XX                 XX",
"XX  XXXXXX  XXX  XX     X",
"XX  XXXXXX  X X  XX     X",
"XX    XXXX  X X      XXXX",
"X     XXXX  X XXXXXXXXXXX",
"XXXX           X      XXX",
"XXXX      XX  XX      X X",
"XXXXXXXX XXX  XXXXXX  X X",
"XXXXXXXX XXX XXXXXX  XXXX",
"l     XX    s   XX    XXX",
"XX  XXXX   XXXXXXX      r",
"XX    XX   X          XXX",
"XXXX  XX  XX XXX  XXXXXXX",
"X  X  XX  XXXXXX  XX   XX",
"XX X         XXX       XX",
"XX           X X    XXXXX",
"XXXXXXXXXXX  X XXX     XX",
"XX  XXXXXXX  X         XX",
"XX     XXXX  XXXXX  XXXXX",
"XXX  XXX      X        XX",
"XXX         X X     XXXXX",
"XXX XXXXXX  X X  X   X  X",
"XXX    XXX       XX    XX",
"XXXXXXXXXXXXXbXXXXXXXXXXX"]

maze_walls = []

def create_pen():
    global pen
    pen = turtle.Turtle()
    pen.color('green')
    pen.shapesize(1)
    pen.setheading(90)
    return pen


def draw_maze(maze):
    global start_x, start_y, top, bottom, left, right, pen     # set up global variables for start location
    pen = create_pen()

    ninja = turtle
    ninja.ht()
    ninja.shape('square')
    ninja.color('black')
    ninja.shapesize()
    ninja.speed(0)
    ninja.penup()
    
    for y in range(len(maze)):                 
        for x in range(len(maze[y])):          
            character = maze[y][x]            
            screen_x = -288 + (x * 24)         
            screen_y = 288 - (y * 24)          

            if character == "X":
                ninja.goto(screen_x, screen_y)         
                ninja.stamp()                          
                walls.append((screen_x, screen_y))    
            
            if character == " " or character in exits :
                path.append((screen_x, screen_y))     

            if character == 't':
                top = (screen_x,screen_y)
                path.append((screen_x, screen_y))     
            
            elif character == 'b':
                bottom = (screen_x,screen_y)
                path.append((screen_x, screen_y))     
 
            elif character == 'l':
                left = (screen_x,screen_y)
                path.append((screen_x, screen_y))     
  
            elif character == 'r':
                right = (screen_x,screen_y)
                path.append((screen_x, screen_y))     
    
            if character == "s":
                start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                pen.goto(screen_x, screen_y)
                path.append((screen_x, screen_y))     
                

def load_maze(maze):
    global start_x, start_y, top, bottom, left, right     # set up global variables for start location
    for y in range(len(maze)):                 # read in the grid line by line
        for x in range(len(maze[y])):          # read each cell in the line
            character = maze[y][x]             # assign the varaible "character" the the x and y location od the grid
            screen_x = -288 + (x * 24)         # move to the x location on the screen staring at -588
            screen_y = 288 - (y * 24)          # move to the y location of the screen starting at 288

            if character == "X":
                walls.append((screen_x, screen_y))    # add coordinate to walls list
        
                
            if character == " " or character in exits :
                path.append((screen_x, screen_y))     # add " " and e to path list
                
            if character == 't':
                top = (screen_x,screen_y)
                path.append((screen_x, screen_y))
                             
            elif character == 'b':
                bottom = (screen_x,screen_y)
                path.append((screen_x, screen_y))
                
            elif character == 'l':
                left = (screen_x,screen_y)
                path.append((screen_x, screen_y))              
                
            elif character == 'r':
                right = (screen_x,screen_y)
                path.append((screen_x, screen_y))

            if character == "s":
                start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                path.append((screen_x, screen_y))
                
load_maze(maze)