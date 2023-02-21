import unittest
from world.obstacles import get_obstacles
from robot import *
from unittest.mock import patch
from io import StringIO

class test_obstacles(unittest.TestCase):
    
    def test_is_int(self):
        self.assertTrue(is_int(2))

    @patch("sys.stdin", StringIO("Hal\n"))
    def test_get_robot_name(self):
        self.assertEqual(get_robot_name(), 'Hal')


    def test_split_command(self):
        self.assertEqual(split_command_input('forward 10'), ('forward', '10'))
        self.assertEqual(split_command_input('back 10'), ('back', '10'))
        self.assertEqual(split_command_input('sprint 15'), ('sprint', '15'))

    def tests_is_int(self):
        self.assertTrue(is_int(10))
        self.assertTrue(is_int(100))
        self.assertFalse(is_int('q'))
        self.assertFalse(is_int('i'))

    def test_is_valid_cmd(self):
        self.assertFalse(valid_command('forward abc'))
        self.assertTrue(valid_command('forward 10'))
        self.assertTrue(valid_command('back 10'))
        self.assertFalse(valid_command('jump up :)'))

    def test_do_help(self):
        help_msg = """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""
        self.assertEqual(do_help()[1], help_msg)

    def test_turn_left(self):
        self.assertEqual(do_left_turn('hal')[1], ' > hal turned left.')

    def test_handle_cmd(self):
        self.assertFalse(handle_command('hal', 'off'), False)

    
