from pickle import TRUE
import sys
from import_helper import dynamic_import
from world import obstacles
from world.text.world import results
from world.text import world
from maze import obstacles as maze_obst
from collections import deque


#Setup global variables
is_turtle = False
is_maze = False
is_text = False
# list of valid command names
valid_commands = ['off', 'help', 'replay', 'forward', 'back', 'right', 'left', 'sprint', 'mazerun']
move_commands = valid_commands[3:]
name = ''
solution = {}
trav_path = deque()
visited = []

if len(sys.argv) == 1:
    is_text = True
    
elif (len(sys.argv) == 2) and (sys.argv[1] == "text"):
    is_text = True

elif (len(sys.argv) == 3) and (sys.argv[2] == "my_maze") and (sys.argv[1] == "turtle"):
    from maze import the_amazing_race as ninja_turtle
    from maze.the_amazing_race import *
    draw_maze(maze)
    is_maze = True
    is_turtle = True
    world.min_x = -288
    world.max_x = 288
    world.min_y = -288
    world.max_y = 288
    
elif (sys.argv[1] == "turtle") and (len(sys.argv) == 2):
    from world.text import world
    from world.turtle import world as ninja_turtle
    is_turtle = True
    
elif (len(sys.argv) == 3) and (sys.argv[1] == "text") and (sys.argv[2] == "my_maze"):
    is_text = True
    is_maze = True
    is_turtle = False
    world.min_x = -288
    world.max_x = 288
    world.min_y = -288
    world.max_y = 288


def get_robot_name():
    global my_obstacles
    global name 
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)
    
    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """
    edges = ['top', 'bottom', 'left', 'right']
    
    (command_name, arg1) = split_command_input(command)
    
    if command_name.lower() == 'replay':
        if len(arg1.strip()) == 0:
            return True
        elif (arg1.lower().find('silent') > -1 or arg1.lower().find('reversed') > -1) and len(arg1.lower().replace('silent', '').replace('reversed','').strip()) == 0:
            return True
        else:
            range_args = arg1.replace('silent', '').replace('reversed','')
            if is_int(range_args):
                return True
            else:
                range_args = range_args.split('-')
                return is_int(range_args[0]) and is_int(range_args[1]) and len(range_args) == 2
    
    elif command_name.lower() == 'mazerun' and arg1.lower() in edges:
        return True
    else:
        return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1))


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """    
    if world.obstacle_check(steps, is_maze):
            return True, ''+robot_name+": Sorry, there is an obstacle in the way."

    if world.update_position(steps):
        if is_turtle:
            ninja_turtle.pen.forward(int(steps))

        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:  
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
        

def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    print(f'Is maze: {is_maze}')
    if world.obstacle_check(-steps, is_maze):
                return True, ''+robot_name+": Sorry, there is an obstacle in the way."

    if world.update_position(-steps):
        if is_turtle:
            ninja_turtle.pen.back(int(steps))
            
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
        

def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    if is_turtle:
        ninja_turtle.pen.right(90)
    world.current_direction_index += 1
    if world.current_direction_index > 3:
        world.current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    if is_turtle:
        ninja_turtle.pen.left(90)
    world.current_direction_index -= 1
    if world.current_direction_index < 0:
        world.current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def get_commands_history(reverse, relativeStart, relativeEnd):
    """
    Retrieve the commands from history list, already breaking them up into (command_name, arguments) tuples
    :param reverse: if True, then reverse the list
    :param relativeStart: the start index relative to the end position of command, e.g. -5 means from index len(commands)-5; None means from beginning
    :param relativeEnd: the start index relative to the end position of command, e.g. -1 means from index len(commands)-1; None means to the end
    :return: return list of (command_name, arguments) tuples
    """

    commands_to_replay = [(name, args) for (name, args) in list(map(lambda command: split_command_input(command), history)) if name in move_commands]
    if reverse:
        commands_to_replay.reverse()

    range_start = len(commands_to_replay) + relativeStart if (relativeStart is not None and (len(commands_to_replay) + relativeStart) >= 0) else 0
    range_end = len(commands_to_replay) + relativeEnd if  (relativeEnd is not None and (len(commands_to_replay) + relativeEnd) >= 0 and relativeEnd > relativeStart) else len(commands_to_replay)
    return commands_to_replay[range_start:range_end]


def do_replay(robot_name, arguments):
    """
    Replays historic commands
    :param robot_name:
    :param arguments a string containing arguments for the replay command
    :return: True, output string
    """

    silent = arguments.lower().find('silent') > -1
    reverse = arguments.lower().find('reversed') > -1
    range_args = arguments.lower().replace('silent', '').replace('reversed', '')

    range_start = None
    range_end = None

    if len(range_args.strip()) > 0:
        if is_int(range_args):
            range_start = -int(range_args)
        else:
            range_args = range_args.split('-')
            range_start = -int(range_args[0])
            range_end = -int(range_args[1])

    commands_to_replay = get_commands_history(reverse, range_start, range_end)

    for (command_name, command_arg) in commands_to_replay:
        (do_next, command_output) = call_command(command_name, command_arg, robot_name)
        if not silent:
            print(command_output)
            world.show_position(robot_name)

    return True, ' > '+robot_name+' replayed ' + str(len(commands_to_replay)) + ' commands' + (' in reverse' if reverse else '') + (' silently.' if silent else '.')


def call_command(command_name, command_arg, robot_name):
    if command_name == 'help':
        return do_help()
    elif command_name == 'forward':
        f_return = do_forward(robot_name, int(command_arg))
    
        if 'Sorry' in f_return[1]: #Checks if the output does allow movement
            return f_return
        else: 
            return f_return
            
    elif command_name == 'back':
        b_return = do_back(robot_name, int(command_arg))

        if 'Sorry' in b_return[1]:
            return b_return
        else:
            if is_turtle:
                ninja_turtle.pen.back(int(command_arg))
            return b_return
        
    elif command_name == 'right':
        return do_right_turn(robot_name)
    elif command_name == 'left':
        return do_left_turn(robot_name)
    elif command_name == 'sprint':
        return do_sprint(robot_name, int(command_arg))
    elif command_name == 'replay':
        return do_replay(robot_name, command_arg)
    return False, None


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """

    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        world.position_x = 0
        world.position_y = 0
        world.current_direction_index = 0
        obstacles.my_obstacles = []
        return False
    
    elif command_name == 'mazerun':
        (do_next, command_output) = mazerun(arg, is_turtle)
        
    else:
        (do_next, command_output) = call_command(command_name, arg, robot_name)

    print(command_output)
    world.show_position(robot_name)
    add_to_history(command)

    return do_next


def add_to_history(command):
    """
    Adds the command to the history list of commands
    :param command:
    :return:
    """
    history.append(command)


def bfs_search(x,y):
    global solution
    from maze.the_amazing_race import path
    trav_path.append((x, y))
    solution[x,y] = x,y

    while len(trav_path) > 0:        
        x, y = trav_path.popleft()    

        if(x - 24, y) in path and (x - 24, y) not in visited:  # check the cell on the left
            cell = (x - 24, y)
            solution[cell] = x, y   
            trav_path.append(cell)  
            visited.append((x-24, y)) 

        if (x, y - 24) in path and (x, y - 24) not in visited:  # check the cell down
            cell = (x, y - 24)
            solution[cell] = x, y
            trav_path.append(cell)
            visited.append((x, y - 24))

        if(x + 24, y) in path and (x + 24, y) not in visited:   # check the cell on the  right
            cell = (x + 24, y)
            solution[cell] = x, y
            trav_path.append(cell)
            visited.append((x +24, y))

        if(x, y + 24) in path and (x, y + 24) not in visited:  # check the cell up
            cell = (x, y + 24)
            solution[cell] = x, y
            trav_path.append(cell)
            visited.append((x, y + 24))

def mazerun_text(destination):
    global solution
    from maze.the_amazing_race import start_x, start_y, create_pen, top, bottom, left, right
    
    bfs_search(start_x, start_y)

    finish = ''
        
    if destination == "top":
        x,y = top
        finish = 'I am at the top edge'
        
    elif destination == "bottom":
        x,y = bottom
        finish = 'I am at the bottom edge'
        
    elif destination == "left":
        x,y = left
        finish = 'I am at the left edge'
        
    elif destination == "right":
        x,y = right
        finish = 'I am at the right edge'
        
    else:
        x,y = top
        finish = 'I am at the top edge'


    print('starting maze run..')
    short_path = []
    
#Loop gets shortest path by going to end position and backtracking to start position
    while (x, y) != (start_x, start_y):    
        short_path.append(solution[x,y])
        x, y = solution[x, y]

    short_path.reverse()

    if destination == "top":
        short_path.append(top)
        
    elif destination == "bottom":
        short_path.append(bottom)
    
    elif destination == "left":
        short_path.append(left)

    elif destination == "right":
        short_path.append(right)
        
    else:
        short_path.append(top)
    
    for position in short_path:
        pass
    
    return finish

def mazerun(destination, turtle):
    """This function will enable the robot to run through the maze and solve it without user interaction
    Args:
        robot_name (STRING): name of the robot
        destination (STRING): the edge at which the robot must goto
        turtle (BOOLEAN): Determines if it's in a turtle world or text only
    """
    
    global solution
    
    from maze.the_amazing_race import start_x, start_y, create_pen, top, bottom, left, right
    
    bfs_search(start_x, start_y)
    
    finish = ''
    
    if turtle:
        
        pen = create_pen()
        
        if destination == "top":
            x,y = top
            finish = 'I am at the top edge'
            
        elif destination == "bottom":
            x,y = bottom
            finish = 'I am at the bottom edge'
            
        elif destination == "left":
            x,y = left
            finish = 'I am at the left edge'
            
        elif destination == "right":
            x,y = right
            finish = 'I am at the right edge'
            
        else:
            x,y = top
            finish = 'I am at the top edge'


        print('starting maze run..')
        short_path = []

    #Loop gets shortest path by going to end position and backtracking to start position
        while (x, y) != (start_x, start_y):    
            short_path.append(solution[x,y])
            x, y = solution[x, y]

        short_path.reverse()

        if destination == "top":
            short_path.append(top)
            
        elif destination == "bottom":
            short_path.append(bottom)
        
        elif destination == "left":
            short_path.append(left)

        elif destination == "right":
            short_path.append(right)
            
        else:
            short_path.append(top)
        
        for position in short_path:
            pen.shape('circle')
            pen.shapesize(0.2)
            pen.goto(position)
    else:
        finish = mazerun_text(destination)    
        
    world.position_x = ""
    world.position_y = ""
    return True, finish


def load_obstacles(text, ninja, turtle, robot_name):
    """Function loads obstacles based on world the robot is in.
    Args:
        text (BOOL): Boolean that is either true for text based world or false
        my_maze (BOOL): Boolean that is either true for the maze world or false
        turtle (BOOL): Boolean that is eithre true for the turtle world or false
    """
    global my_obstacles
    
    if text and ninja:
        from maze.the_amazing_race import walls, load_maze, maze
        load_maze(maze)
        my_obstacles = walls 
        print(f"{robot_name}: Loaded my_maze.")

    elif turtle and ninja:
        from maze.the_amazing_race import walls, maze
        my_obstacles = walls
        
    elif text:
        my_obstacles = obstacles.get_obstacles()
        obstacles.assign_obstacles(my_obstacles)
        print(f'{robot_name}: Loaded obstacles.')
        
    elif turtle:
        my_obstacles = obstacles.get_obstacles()
        obstacles.assign_obstacles(my_obstacles)
        ninja_turtle.positions = my_obstacles
        
        for i in range(len(my_obstacles)):
            ninja_turtle.place_obstacle(ninja_turtle.positions[i])
    else: 
        my_obstacles = obstacles.get_obstacles()
        obstacles.assign_obstacles(my_obstacles)
        print(f'{robot_name}: Loaded obstacles.')


def robot_start():
    """This is the entry point for starting my robot"""
    global position_x, position_y, current_direction_index, history, is_turtle, my_obstacles
    my_obstacles = []
    history = []
    position_x = 0
    position_y = 0
    current_direction_index = 0
    history = []
    
    robot_name = get_robot_name()
    
    output(robot_name, "Hello kiddo!")
    
    load_obstacles(is_text, is_maze, is_turtle, robot_name)
    
    if is_maze:
        maze_obst.assign_obstacles(my_obstacles)
    else:
        obstacles.assign_obstacles(my_obstacles)
            
    if len(my_obstacles) > 0 and not is_turtle:
        results(my_obstacles)
    elif len(my_obstacles) > 0 and is_maze and is_text:
        results(my_obstacles)
    elif len(my_obstacles) > 0 and is_text:
        results(my_obstacles)
    
    command = get_command(robot_name)
    
    while handle_command(robot_name, command):
        command = get_command(robot_name)

    output(robot_name, "Shutting down..")

if __name__ == "__main__":
    robot_start()