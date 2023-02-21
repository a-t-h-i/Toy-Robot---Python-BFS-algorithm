import unittest
from world.obstacles import get_obstacles
from world.obstacles import *

class test_obstacles(unittest.TestCase):
    my_obstacles = get_obstacles()    
    def test_get_obstacles(self):
        self.assertEqual(bool(my_obstacles), False)

    def test_position_blocked(self):
        my_obstacles = [[(13, 162), (17, 162), (17, 166), (13, 166)]]
        self.assertFalse(is_position_blocked(50, 10))
        self.assertFalse(is_position_blocked(100,200))