import unittest, io, sys
from world.text.world import *
from world.text.world import is_position_allowed, update_position

class test_obstacles(unittest.TestCase):
    
    def test_is_postition_allowed(self):
        sys.stdout = io.StringIO()
        self.assertTrue(is_position_allowed(1,1))
        self.assertFalse(is_position_allowed(1,300))
        self.assertFalse(is_position_allowed(-300,200))
        self.assertTrue(is_position_allowed(100,200))

    def test_update_position(self):
        self.assertTrue(update_position(100))
        self.assertFalse(update_position(201))

    

    
