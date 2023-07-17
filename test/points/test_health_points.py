import unittest
from points.health_point import HealthPoint

class HealthPointTest(unittest.TestCase):

    def setUp(self):
        self.point = HealthPoint(1)

    def test_return_val(self):
        self.assertEqual(self.point.return_val(), 1)
    
    @unittest.expectedFailure
    def test_return_wrong_val(self):
        self.assertEqual(self.point.return_val(), 3)

if __name__ == '__main__':
    unittest.main()