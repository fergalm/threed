from .bbox import Bbox 

#TODO: Should I specify platescale instead of fov?
class Detector(Bbox):
    def __init__(self, hoffset, woffset, height, width, horz_fov_degrees):
        Bbox.__init__(self, hoffset, woffset, height, width)
        self.horz_fov_degrees = horz_fov_degrees
        """Field of view, from extreme left, to extreme right, in degrees"""

    @classmethod 
    def from_coords(col1, col2, row1, row2, horz_fov_degrees):
        det = Bbox.from_coords( col1, col2, row1, row2)
        det.horz_fov_degrees = horz_fov_degrees 
        return det 


