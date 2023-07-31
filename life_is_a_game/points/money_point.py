from life_is_a_game.points.point import Point
from life_is_a_game.points.point_type import PointType

class MoneyPoint(Point):

    def __init__(self, val):
        super().__init__(val, PointType.MONEY.value)