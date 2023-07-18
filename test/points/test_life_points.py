import unittest
from points.life_point import LifePoint

class LifePointTest(unittest.TestCase):

    def setUp(self):
        self.point = LifePoint(1)

    def test_return_val(self):
        self.assertEqual(self.point.return_val(), 1)
    
    @unittest.expectedFailure
    def test_return_wrong_val(self):
        self.assertEqual(self.point.return_val(), 3)

if __name__ == '__main__':
    unittest.main()