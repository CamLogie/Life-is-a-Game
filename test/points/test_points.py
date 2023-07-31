import unittest
from life_is_a_game.points.point import Point

class PointTest(unittest.TestCase):

    def setUp(self):
        self.point = Point(1, 'test')

    def test_return_val(self):
        self.assertEqual(self.point.val, 1)
    
    @unittest.expectedFailure
    def test_return_wrong_val(self):
        self.assertEqual(self.point.val, 3)
    
    def test_return_point_type(self):
        self.assertEqual(self.point.point_type, 'test')
    
    def test_cannot_set_point_type(self):
        with self.assertRaises(AttributeError):
            self.point.point_type = 'test2'

if __name__ == '__main__':
    unittest.main()