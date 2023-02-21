import random
# from robot import my_obstacles
min_y, max_y = -288, 288
min_x, max_x = -288, 288
my_obstacles = []

def assign_obstacles(obstacles):
    global my_obstacles
    my_obstacles = obstacles


def is_position_blocked(x,y):
    """Function returns True if position (x,y) falls inside an obstacle.
    Args:
        x ([int]): The x coordinates
        y ([int]): The y coordinates 
    """
    for i in range(len(my_obstacles)):
        if x in range(my_obstacles[i][0], my_obstacles[i][0]+24) and y in range(my_obstacles[i][1], my_obstacles[i][1]+24):
            return True
    return False
    
    
def  is_path_blocked(start_x,start_y, end_x, end_y):
    """Function returns True if there is an obstacle in the line between
       the coordinates (start_x, start_y) and (end_x, end_y)
    """
    if start_y < end_y:
        for y_count in range(start_y,end_y):
            if is_position_blocked(start_x, y_count):
                return True
    else:
        #If start is greater than end
        for y_count in range(end_y,start_y):
            if is_position_blocked(start_x, y_count):
                return True
            
    if start_x < end_x:
        for x_count in range(start_x,end_x):
            if is_position_blocked(x_count,start_y):
                return True
    else:
        #If start is greater than end
        for x_count in range(end_x,start_x):
            if is_position_blocked(x_count,start_y):
    
                    return True
    return False
   
   
def get_obstacles():
    """Function returns an obstacle
    """ 
    obstacles = []
    #Random positions to place obstacles
    for i in range(random.randint(1,10)):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        obstacles.append((x,y))
    
    return obstacles