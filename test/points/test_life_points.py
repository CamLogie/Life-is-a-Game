import unittest
from life_is_a_game.points.life_point import LifePoint

class LifePointTest(unittest.TestCase):

    def setUp(self):
        self.point = LifePoint(1)

    def test_return_val(self):
        self.assertEqual(self.point.val, 1)
    
    @unittest.expectedFailure
    def test_return_wrong_val(self):
        self.assertEqual(self.point.val, 3)

if __name__ == '__main__':
    unittest.main()