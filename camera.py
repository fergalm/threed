from ipdb import set_trace as idebug
import numpy as np 

from element import Element

class Camera(Element):
    #TODO Implement FOV
    def __init__(self):
        self.pos = np.array([0,0,0,1])
        self.attitude = np.array([0,0,0,1])

