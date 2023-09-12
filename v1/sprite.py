from ipdb import set_trace as idebug
import numpy as np 
from element import Element



class Sprite(Element):
    def __init__(self, pos, attitude):
        self.pos = pos 
        self.attitude = attitude
        self.colours = None 


    def getEnvelope(self):
        return np.array([ 
            [-1,-1,-1,1],
            [-1,+1,-1,1],
            [+1,+1,-1,1],
            [+1,-1,-1,1],
            [-1,-1,+4,1],
            [-1,+1,+4,1],
            [+1,+1,+4,1],
            [+1,-1,+4,1],
        ])

    def getFacets(self):
        return self.facets 
    
    def getPoints(self):
        return self.points 

    def getPosition(self):
        return self.pos 

    def getAttitude_rad(self):
        return self.attitude

    def setAttitude_rad(self, ang):
        self.attitude = ang


class Pyramid(Sprite):
    """Simplet possible Sprite"""
        # self.pos = np.array([4,5,2,1])
    def __init__(self):
        self.pos = np.array([4,0,0,1])
        # self.attitude = np.radians([30, 0, 30])

        pp = np.sqrt(3)/2
        self.points = np.array([ 
            [-pp, -.5, -pp, 1],
            [+pp, -.5, -pp, 1],
            [0,     1, -pp, 1],
            [0,     0, 2.23, 1]
        ])

        self.facets = np.array(
            [
                [0,1,2],
                [0,1,3],
                [1,2,3],
                [0,2,3],
            ],
            dtype=np.int16
        )

        self.colours = np.array('r g b c'.split())
