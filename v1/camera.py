from ipdb import set_trace as idebug
import numpy as np 

from element import Element

class Camera(Element):
    #TODO Implement FOV
    def __init__(self, plateScale_arcsecPerPixel):
        assert plateScale_arcsecPerPixel > 0
        self.platescale_arcsecPerPixel =  plateScale_arcsecPerPixel
        self.platescale_radPerPix = \
            np.radians(plateScale_arcsecPerPixel * 3600)

        self.pos = np.array([0,0,0,1])
        self.attitude = np.array([0,0,0,1])
