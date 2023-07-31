class Point(object):
    def __init__(self, val, point_type):
        self.val = val
        self._point_type = point_type
    
    @property
    def point_type(self):
        return self._point_type


    
