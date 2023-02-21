# from robot import is_position_blocked, is_path_blocked
from world.obstacles import is_path_blocked, is_position_blocked
from maze import obstacles as maze_obst


# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

new_x = position_x
new_y = position_y

min_y, max_y = -200, 200
min_x, max_x = -100, 100


def results(positions):
    
    if len(positions) > 0:
        
        print('There are some obstacles:')
        for i in range(len(positions)):
            print(f"- At position {positions[i][0]},{positions[i][1]} (to {positions[i][0] + 4},{positions[i][1] + 4})")

            
def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')

def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    return min_x <= new_x <= max_x and min_y <= new_y <= max_y

def obstacle_check(steps, is_maze):
    global x2, y2, x1, y1, new_x, new_y
    
    new_x = position_x
    new_y = position_y
    
    x1 = position_x
    y1 = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps

    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps

    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps

    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        x2 = new_x 
        y2 = new_y
    else:
        x2 = 0
        y2 = 0
        
    if is_maze:
        position_blocked = maze_obst.is_position_blocked(new_x, new_y)
        path_blocked = maze_obst.is_path_blocked(x1, y1, x2, y2)    
    
    else:    
        position_blocked = is_position_blocked(new_x, new_y)
        path_blocked = is_path_blocked(x1, y1, x2, y2)
    
    if position_blocked or path_blocked:
        return True
    else:
        return False

def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """
    global position_x, position_y, position_blocked, path_blocked, x2, y2, x1, y1, new_x, new_y
    new_x = position_x
    new_y = position_y
    
    x1 = position_x
    y1 = position_y
    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps

    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps

    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps

    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    
    if is_position_allowed(new_x, new_y):
        position_x = new_x
        x2 = position_x
        position_y = new_y
        y2 = position_y
        return True
        
    return False